import re

from click import option

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

def create_template(fes = [], dbs = [], separate_db=False):
    compose = { 'main': '', 'db': '' }
    compose['main'] += read_file('prefabs/head.yml')
    for k in fes:
        compose['main'] += read_file(f"prefabs/{k}/compose.yml")
    if separate_db == True:
        compose['db'] += read_file('prefabs/head.yml')
        target = 'db'
    else:
        target = 'main'
    for k in dbs:
        print(k)
        compose[target] += read_file(f"prefabs/{k}/compose.yml")
    compose['main'] += read_file('prefabs/tail.yml')
    if separate_db == True:
        compose['db'] += read_file('prefabs/tail.external.yml')
    print(f"Generated\nFEA: {fes}\nDBS: {dbs}\nSDB: {separate_db}")
    return compose

def create_template2(
    has_vue = False,
    has_django = False,
    has_nodejs = False,
    has_postgres = False,
    has_mongo = False,
    has_mongors = False,
    has_separate_db = False
):
    compose = { 'main': '', 'db': ''}
    compose['main'] += read_file('prefabs/head.yml')
    if has_vue == True:
        compose['main'] += read_file('prefabs/vue/compose.yml')
    if has_django == True:
        compose['main'] += read_file('prefabs/django/compose.yml')
    if has_nodejs == True:
        compose['main'] += '\n#NodeJS here\n'
    if has_separate_db == False:
        if has_postgres == True:
            compose['main'] += read_file('prefabs/postgres/compose.yml')
        if has_mongo == True:
            compose['main'] += '\n#MongoDB here\n'
        if has_mongors == True:
            compose['main'] += '\n#MongoDB Replica Set here\n'
    else:
        compose['db']  += read_file('prefabs/head.yml')
        if has_postgres == True:
            compose['db']  += read_file('prefabs/postgres/compose.yml')
        if has_mongo == True:
            compose['db']  += '\n#MongoDB here\n'
        if has_mongors == True:
            compose['db']  += '\n#MongoDB Replica Set here\n'
        compose['db']  += read_file('prefabs/tail.external.yml')
    compose['main'] += read_file('prefabs/tail.yml')
    # re.sub(r"^\s+", '', compose)

    return compose

print('generate.py loaded')