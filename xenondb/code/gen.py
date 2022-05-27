import os
import json

# get current work path
root_path = os.getcwd()

# Insert a str type value into "%s" location
children = '{"name":"%s.py", "children": [], "type":"file"}'

# directory construction
dir_map = [{
    'name':'xenondb',
    'type':'dir',
    'children':[
        json.loads(children % '__init__'),
        json.loads(children % '__main__'),
        {
            'name':'case',
            'type':'dir',
            'children':[json.loads(children % '__init__')]
        },
        {
            'name':'parser',
            'type':'dir',
            'children':[json.loads(children % '__init__')]
        },
        {
            'name': 'exceptions',
            'type': 'dir',
            'children': [json.loads(children % '__init__')]
        },
        {
            'name': 'core',
            'type': 'dir',
            'children': [json.loads(children % '__init__'), json.loads(children % 'field'), json.loads(children % 'database'), json.loads(children % 'table'), json.loads(children % '__init__')]
        },
    ]
}]

def create(path, kind):
    if kind == "dir":
        os.mkdir(path)
    else:
        open(path, "w").close()


# recrusively generate directory
def gen_project(parent_path, map_obj):
    for line in map_obj:
        print(line)
        # join the path and file name
        path = os.path.join(parent_path, line['name'])
        create(path, line['type'])
        if line['children']:
            gen_project(path, line['children'])

def main():
    gen_project(root_path, dir_map)

if __name__ == "__main__":
    main()