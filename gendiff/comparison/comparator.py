import json
import yaml
# dump -> cast to string
# load -> cast to document


def get_diff(first_file, second_file):
    (file1, file2) = get_files(first_file, second_file)
    # print(file1)
    # print(file2)
    result = run_diff(file1, file2)
    # print(result)
    print(''.join(json.dumps(result, indent=2).split('"')))


def get_files(first_file, second_file):
    file1 = yaml.load(open(first_file), yaml.Loader)
    file2 = yaml.load(open(second_file), yaml.Loader)
    return (file1, file2)


def run_diff(file1, file2):
    result = {}
    for k in file1:
        if k in file1 and k in file2:
            if type(file1[k]) is dict and type(file1[k]) is dict:
                result[f'  {k}'] = run_diff(file1[k], file2[k])
            elif file2[k] == file1[k]:
                result[f'  {k}'] = file1[k]
            else:
                result[f'- {k}'] = file1[k]
                result[f'+ {k}'] = file2[k]
        elif k in file1:
            result[f'- {k}'] = file1[k]
    for k in file2:
        if not k in file1:
            result[f'+ {k}'] = file2[k]
    return result