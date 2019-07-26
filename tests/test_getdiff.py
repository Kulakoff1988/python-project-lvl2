import pytest
import json
from gendiff import engine

def test_empty():
    assert None == engine.get_diff(
        './tests/fixtures/test_empty1.json',
        './tests/fixtures/test_empty2.json'
    )
    assert None == engine.get_diff(
        './tests/fixtures/test_empty1.yml',
        './tests/fixtures/test_empty2.yml'
    )


def test_flat_files():
    string_result = ('{\n'
        '    constant: yep\n'
        '  - test: bar\n'
        '  + test: foo\n'
        '  - foo: bar\n'
        '  + bar: foo\n'
    '}')
    plain_result = (
        'Property "test" was changed. From "bar" to "foo"\n'
        'Property "foo" was removed\n'
        'Property "bar" was added with value: "foo"'
    )
    json_result = json.dumps({
        'constant': 'yep',
        '- test': 'bar',
        '+ test': 'foo',
        '- foo': 'bar',
        '+ bar': 'foo'
    })
    assert string_result == engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json'
    )
    assert plain_result == engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json',
        'plain'
    )
    assert json_result == engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json',
        'json'
    )
    assert string_result == engine.get_diff(
        './tests/fixtures/test1.yml',
        './tests/fixtures/test2.yml'
    )
    assert plain_result == engine.get_diff(
        './tests/fixtures/test1.yml',
        './tests/fixtures/test2.yml',
        'plain'
    )
    assert json_result == engine.get_diff(
        './tests/fixtures/test1.yml',
        './tests/fixtures/test2.yml',
        'json'
    )


def test_nested_files():
    string_result = ('{\n'
        '    common: {\n'
        '        setting1: Value 1\n'
        '      - setting2: 200\n'
        '        setting3: true\n'
        '      - setting6: {\n'
        '            key: value\n'
        '        }\n'
        '      + setting4: blah blah\n'
        '      + setting5: {\n'
        '            key5: value5\n'
        '        }\n'
        '    }\n'
        '    group1: {\n'
        '      - baz: bas\n'
        '      + baz: bars\n'
        '        foo: bar\n'
        '    }\n'
        '  - group2: {\n'
        '        abc: 12345\n'
        '    }\n'
        '  + group3: {\n'
        '        fee: 100500\n'
        '    }\n'
    '}')
    plain_result = (
        'Property "common.setting2" was removed\n'
        'Property "common.setting6" was removed\n'
        'Property "common.setting4" was added with value: "blah blah"\n'
        'Property "common.setting5" was added with value: "complex value"\n'
        'Property "group1.baz" was changed. From "bas" to "bars"\n'
        'Property "group2" was removed\n'
        'Property "group3" was added with value: "complex value"'
    )
    json_result = json.dumps({
        'common': {
            'setting1': 'Value 1',
            '- setting2': '200',
            'setting3': 'true',
            '- setting6': {
                'key': 'value'
            },
            '+ setting4': 'blah blah',
            '+ setting5': {
                'key5': 'value5'
            }
        },
        'group1': {
            '- baz': 'bas',
            '+ baz': 'bars',
            'foo': 'bar'
        },
        '- group2': {
            'abc': '12345'
        },
        '+ group3': {
            'fee': '100500'
        }
    })
    assert string_result == engine.get_diff(
        './tests/fixtures/test1.json',
        './tests/fixtures/test2.json'
    )
    assert plain_result == engine.get_diff(
        './tests/fixtures/test1.json',
        './tests/fixtures/test2.json',
        'plain'
    )
    assert json_result == engine.get_diff(
        './tests/fixtures/test1.json',
        './tests/fixtures/test2.json',
        'json'
    )