import pytest
import json
from gendiff import engine

STRING_RESULT_FLAT = '''{
    constant: yep
  - test: bar
  + test: foo
  - foo: bar
  + bar: foo
}'''

STING_RESULT_NESTED = '''{
    common: {
        setting1: Value 1
      - setting2: 200
        setting3: true
      - setting6: {
            key: value
        }
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
    }
  - group2: {
        abc: 12345
    }
  + group3: {
        fee: 100500
    }
}'''

PLAIN_RESULT_FLAT = '''Property "test" was changed. From "bar" to "foo"
Property "foo" was removed
Property "bar" was added with value: "foo"'''

PLAIN_RESULT_NESTED = '''Property "common.setting2" was removed
Property "common.setting6" was removed
Property "common.setting4" was added with value: "blah blah"
Property "common.setting5" was added with value: "complex value"
Property "group1.baz" was changed. From "bas" to "bars"
Property "group2" was removed
Property "group3" was added with value: "complex value"'''

JSON_RESULT_FLAT = json.dumps({
    'constant': 'yep',
    '- test': 'bar',
    '+ test': 'foo',
    '- foo': 'bar',
    '+ bar': 'foo'
})

JSON_RESULT_NESTED = json.dumps({
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


# def test_empty():
#     assert engine.get_diff(
#         './tests/fixtures/test_empty1.json',
#         './tests/fixtures/test_empty2.json',
#         'string'
#     ) is None
#     assert engine.get_diff(
#         './tests/fixtures/test_empty1.yml',
#         './tests/fixtures/test_empty2.yml',
#         'string'
#     ) is None


def test_flat_files():
    assert engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json',
        'string'
    ) == STRING_RESULT_FLAT
    # assert engine.get_diff(
    #     './tests/fixtures/test_flat1.json',
    #     './tests/fixtures/test_flat2.json',
    #     'plain'
    # ) == PLAIN_RESULT_FLAT
    # assert engine.get_diff(
    #     './tests/fixtures/test_flat1.json',
    #     './tests/fixtures/test_flat2.json',
    #     'json'
    # ) == JSON_RESULT_FLAT
    assert engine.get_diff(
        './tests/fixtures/test1.yml',
        './tests/fixtures/test2.yml',
        'string'
    ) == STRING_RESULT_FLAT
    # assert engine.get_diff(
    #     './tests/fixtures/test1.yml',
    #     './tests/fixtures/test2.yml',
    #     'plain'
    # ) == PLAIN_RESULT_FLAT
    # assert engine.get_diff(
    #     './tests/fixtures/test1.yml',
    #     './tests/fixtures/test2.yml',
    #     'json'
    # ) == JSON_RESULT_FLAT


def test_nested_files():
    assert engine.get_diff(
        './tests/fixtures/test1.json',
        './tests/fixtures/test2.json',
        'string'
    ) == STING_RESULT_NESTED
    # assert engine.get_diff(
    #     './tests/fixtures/test1.json',
    #     './tests/fixtures/test2.json',
    #     'plain'
    # ) == PLAIN_RESULT_NESTED
    # assert engine.get_diff(
    #     './tests/fixtures/test1.json',
    #     './tests/fixtures/test2.json',
    #     'json'
    # ) == JSON_RESULT_NESTED