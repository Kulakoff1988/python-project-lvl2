from gendiff.formatters import string, plain, m_json

JSON_FORMAT = '.json'
YAML_FORMAT = '.yml'

FORMAT_STRING, FORMAT_PLAIN, FORMAT_JSON = ('string', 'plain', 'json')

BUILDERS_FORMATS = {
    FORMAT_STRING: string,
    FORMAT_PLAIN: plain,
    FORMAT_JSON: m_json
}

BLANKS = {
    FORMAT_STRING: lambda: '{\n',
    FORMAT_PLAIN: lambda: [],
    FORMAT_JSON: lambda: {}
}