import re

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def read_file(file):
    with open(file, 'r') as f:
        content = f.read()
    return content


def create_template(fes = [], dbs = [], separate_db=False, tag=''):
    compose = { 'main': '', 'db': '' }
    compose['main'] += read_file('prefabs/head.yml')
    for k in fes:
        compose['main'] += read_file(f"prefabs/{k}/compose.yml")
    if separate_db == 'True':
        compose['db'] += read_file('prefabs/head.yml')
        target = 'db'
    else:
        target = 'main'
    for k in dbs:
        compose[target] += read_file(f"prefabs/{k}/compose.yml")
    compose['main'] += read_file('prefabs/tail.yml')
    if separate_db == 'True':
        compose['db'] += read_file('prefabs/tail.external.yml')
    if tag == 'dev':
        compose['main'] = re.sub(r"#{{hosted}}#.*?#{{endhosted}}#", '', compose['main'], flags=re.DOTALL)
    else:
        compose['main'] = re.sub(r"#{{local}}#.*?#{{endlocal}}#", '', compose['main'], flags=re.DOTALL)
    print(f"Generated compose\nFeatures: {fes}\nDatabases: {dbs}\nSeparate DB: {separate_db}")
    return compose


def create_workflow(fes = [], tag = ''):
    workflow = ''
    workflow += read_file('prefabs/workflow_head.yml')
    for k in fes:
        workflow += read_file(f"prefabs/{k}/workflow.yml")
    workflow += read_file('prefabs/workflow_tail.yml')
    print(f"Generated workflow\nFeatures: {fes}")
    return workflow


def create_dockerfile(feature='', tag=''):
    dockerfile = {'name': '', 'content': ''}
    if tag == 'production':
        suffix = ''
    else:
        suffix = f".{tag}"
    try:
        dockerfile['content'] = read_file(f"prefabs/{feature}/Dockerfile{suffix}")
    except FileNotFoundError:
        print(f"No prefabs/{feature}/Dockerfile{suffix}, using default")
        dockerfile['content'] = read_file(f"prefabs/{feature}/Dockerfile")
    dockerfile['name'] = f"Dockerfile{suffix}"
    print(f"Genearted dockerfile for {feature} - {tag}")
    return dockerfile


print('generate.py loaded')
