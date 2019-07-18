import json
import yaml
# dump -> cast to string
# load -> cast to document


# def get_diff(first_file, secodnd_file):
#     file1 = json.load(open(first_file))
#     file2 = json.load(open(secodnd_file))
#     print(file1)
#     print(file2)
    # result = {}
    # for k in file1:
    #     if k in file1 and k in file2:
    #         if file2[k] == file1[k]:
    #             result[f'  {k}'] = file1[k]
    #         else:
    #             result[f'- {k}'] = file1[k]
    #             result[f'+ {k}'] = file2[k]
    #     elif k in file1:
    #         result[f'- {k}'] = file1[k]
    # for k in file2:
    #     if not k in file1:
    #         result[f'+ {k}'] = file2[k]
    # print(''.join(json.dumps(result, indent=4).split('"')))

def get_diff(first_file, second_file):
    file1 = yaml.load(open(first_file), yaml.Loader)
    file2 = yaml.load(open(second_file), yaml.Loader)
    print(file1)
    print(file2)
    result = {}
    for k in file1:
        if k in file1 and k in file2:
            if file2[k] == file1[k]:
                result[f'  {k}'] = file1[k]
            else:
                result[f'- {k}'] = file1[k]
                result[f'+ {k}'] = file2[k]
        elif k in file1:
            result[f'- {k}'] = file1[k]
    for k in file2:
        if not k in file1:
            result[f'+ {k}'] = file2[k]
    # print(result)
    # print(''.join(yaml.dump(result)))
    print(''.join(json.dumps(result, indent=2).split('"')))