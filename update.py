import sys
import re
import yaml
import json
from yaml.loader import SafeLoader

content_new = ''
with open('helm-simples/templates/deployment.yaml') as file:
    lines = list(file)
    for line in lines:
        #print(line)
        line_formated = line#.replace('\n','')
        pattern = re.compile(r'\{\{-\s([\w]+)[\s\.\|\w]+\}}')
        regex_key = pattern.search(line)
        if regex_key:
            check_indent = re.match(r'\s*', line).group()
            new_key = regex_key.group(1)
            new_value = regex_key.string          
            new_line = f'{check_indent}helm_{new_key}: "{new_value.strip()}"\n'
            content_new += new_line
        elif '{{' in line and ':' in line:
            check_indent = re.match(r'\s*', line).group()
            split_line = line.split(':')
            key = split_line[0]
            value = split_line[-1]
            new_line = f'{key}: "{value.strip()}"\n'
            content_new += new_line
        else:
            content_new += line
    
    print(content_new)
    print('='*10)
    yaml_data = yaml.load(content_new, Loader=SafeLoader)
    resource_metadata = yaml_data.get('metadata')
    resource_labels = resource_metadata.get('labels')
    if resource_labels:
        print(yaml.dump(yaml_data, indent=2))
    else:
        print('Labels not found')
        labels = yaml_data['metadata']['labels'] = {}
        labels['type-project'] = "{{ .Values.type-project }}"
        print(yaml.dump(yaml_data, indent=2))
