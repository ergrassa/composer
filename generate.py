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
    print(f"Generated compose\nFeatures: {fes}\nDatabases: {dbs}\nSeparate DB: {separate_db}")
    return compose

def create_workflow(fes = []):
    workflow = ''
    workflow += read_file('prefabs/workflow_head.yml')
    for k in fes:
        workflow += read_file(f"prefabs/{k}/workflow.yml")
    workflow += read_file('prefabs/workflow_tail.yml')
    print(f"Generated workflow\nFeatures: {fes}")
    return workflow

print('generate.py loaded')