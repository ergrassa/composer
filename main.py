
from flask import Flask, request, render_template, Response
from generate import *
import os, time

(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('./version')
with open('./version', 'r') as f:
    version = f"{str(f.read())} of {time.ctime(mtime)}"

app = Flask(__name__,
            static_url_path='', static_folder='static')  

feat = {
    'Frontend': {
        'vue': 'Vue frontend',
        'vue-docs': 'Docs'
    },
    'Backend': {
        'django': 'Django backend',
        'nodejs': 'NodeJS backend'
    },
    'Database': {
        'postgres': 'PostgreSQL 15',
        'mongo': 'Mongo 6',
        # 'mongors': 'Mongo replica set'
    },
    'Database helpers': {
        'pgadmin': 'Pgadmin',
        'mex': 'Mongo Express'
    }
}
images = {
    'vue': 'frontend',
    'vue-docs': 'docs',
    'django': 'backend',
    'nodejs': 'backend',
}
# kv = {
#     'vue': 'Vue frontend',
#     'django': 'Django backend',
#     'nodejs': 'NodeJS backend',
#     'postgres': 'PostgreSQL database',
#     'mongo': 'Mongo database',
#     'mongors': 'Mongo replica set'
# }
fes = []
dbs = []
for k,v in feat.items():
    if 'Database' in k:
        for i, _ in v.items():
            dbs.append(i)
    else:
        for i,_ in v.items():
            fes.append(i)
print(fes)
print(dbs)

@app.route('/', methods =['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = dict(request.form)
        project = data.get('project')
        # Data replace and format
        f_on = []
        db_on = []
        for k,v in data.items():
            if 'has_' in k and v == 'on':
                data[k] = True
                if re.sub('has_','',k) in fes:
                    f_on.append(re.sub('has_','',k))
                if re.sub('has_','',k) in dbs:
                    db_on.append(re.sub('has_','',k))
        print(f_on)
        print(db_on)
        if data.get('network_name') == '':
            data['network_name'] = project
        envs = []
        for e in ['production', 'staging', 'dev']:
            if data.get(f"has_{e}"):
                envs.append(e)
        if len(envs) == 0:
            return render_template('output.html', payload={'no environment selected': '# no environment selected'})
        #     print('No environment selected')
        #     return 'No environment selected'

        payload = {}
        for tag in envs:
            template = create_template(f_on, db_on, data.get('has_separate_db'), tag = tag)
            compose_name = f"docker-compose.{tag}.yml"
            db_compose_name = f"docker-compose.{tag}.db.yml"
            payload[compose_name] = template['main']
            if tag != 'dev':
                workflow_template = create_workflow(f_on)
                workflow_name = f"deploy.{tag}.yml"
                payload[f"{workflow_name}"] = workflow_template
            if data.get('has_separate_db') == True:
                payload[db_compose_name] = template['db']
            if tag == 'staging':
                suffix = '-staging'
                branch = 'dev'
            elif tag == 'dev':
                suffix = '-dev'
                branch = ''
            else:
                suffix = ''
                branch = 'main'
            pulls = ''
            needs = '['
            # {{org}}/{{project}}-frontend:{{tag}}
            for f in f_on:
                pulls += f"{' '*12}docker pull {data.get('org')}/{data.get('project')}-{images[f]}:{tag}\n"
                needs += f"{images[f]}-build, "
            needs = re.sub(r", $", ']', needs)
            repl = {
                '{{version}}': data.get('compose_version'),
                '{{org}}': data.get('org'),
                '{{project}}': project,
                '{{team}}': data.get('team'),
                '{{email}}': data.get('email'),
                '{{tag}}': tag,
                '{{network_name}}': data.get('network_name'),
                '{{network_driver}}': data.get('network_driver'),
                '{{frontend}}': f"{project}{suffix}.",
                '{{backend}}': f"{project}-backend{suffix}.",
                '{{docs}}': f"{project}-docs{suffix}.",
                '{{domain}}': data.get(f"vhost_{tag}"),
                '{{pgadmin}}': f"{project}-pgadmin{suffix}.",
                '{{mex}}': f"{project}-mex{suffix}.",
                '{{branch}}' : branch,
                '{{engine}}' : data.get(f"engine_{tag}"),
                '{{tag_upper}}' : tag.upper(),
                '{{pulls}}' : pulls.rstrip(),
                '{{needs}}' : needs
            }
            if (data.get(f"engine_{tag}") == '') and (tag != 'dev'):
                payload[workflow_name] = re.sub(r"#{{vault}}#.*?#{{vaultend}}#", '', payload[workflow_name], flags=re.DOTALL)
            print(payload.keys())
            for k,v in repl.items():
                # print(f"{k} : {v}")
                payload[compose_name] = re.sub(k, v, payload[compose_name])
                if data.get('has_separate_db') == True:
                    payload[db_compose_name] = re.sub(k, v, payload[db_compose_name])
                if tag != 'dev':
                    for k,v in repl.items():
                        payload[workflow_name] = re.sub(k, v, payload[workflow_name])
        for k in payload.keys():
            payload[k] = re.sub(r"#{{.+?}}#\n", '', payload[k])
            # payload[k] = re.sub(r"^\s*\n", '', payload[k], flags=re.MULTILINE)
        sorted_payload = dict(sorted(payload.items()))
        return render_template('output.html', payload=sorted_payload, version=version)
    return render_template('index.html', feat=feat, version=version)
 
if __name__=='__main__':
#    app.run()
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)