"""
1. Busca regex com a linha do with
2. Se tiver, proximo arquivo
3. Se não tiver, insere
"""

import re

with open('helm-simples/templates/deployment.yaml') as file:
    lines = list(file)
    new_file = ''
    for line in lines:
        pattern_labels = re.compile(r'\{\{- with .Values.spec.labels }}')
        pattern_labels_empty = re.compile(r'\s*labels: {}')
        check_labels = pattern_labels.search(line)
        check_labels_empty = pattern_labels_empty.search(line)
        check_indent = re.match('\s*', line).group()
        if check_labels:
            print('New template is defined')
            new_file += line
        elif check_labels_empty:
            print('Labels is defined but is empty')
            indent_size = len(check_indent)
            indent = ' '*(indent_size+2)
            new_line = f'{check_indent}labels: \n{indent}'
            new_label_template = ' '*indent_size + 'labels: \n' + indent + '{{- with .Values.spec.labels }}\n' + indent + '{{- toYaml . | nindent 4 }}\n' + indent + '{{- end }}'
            insert = re.sub(pattern_labels_empty, new_label_template, line)
            new_file += insert
        else:
            new_file += line
    print(new_file)
    with open('deployment.yaml', 'w') as output_file:
        output_file.write(new_file)    

