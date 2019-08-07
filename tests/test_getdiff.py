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


def test_flat_files():
    assert engine.get_diff(
        './tests/fixtures/test_flat_old.json',
        './tests/fixtures/test_flat_new.json',
        'string'
    ) == STRING_RESULT_FLAT
    assert engine.get_diff(
        './tests/fixtures/test_flat_old.json',
        './tests/fixtures/test_flat_new.json',
        'plain'
    ) == PLAIN_RESULT_FLAT
    assert engine.get_diff(
        './tests/fixtures/test_flat_old.yml',
        './tests/fixtures/test_flat_new.yml',
        'string'
    ) == STRING_RESULT_FLAT
    assert engine.get_diff(
        './tests/fixtures/test_flat_old.yml',
        './tests/fixtures/test_flat_new.yml',
        'plain'
    ) == PLAIN_RESULT_FLAT


def test_nested_files():
    assert engine.get_diff(
        './tests/fixtures/test_nested_old.json',
        './tests/fixtures/test_nested_new.json',
        'string'
    ) == STING_RESULT_NESTED
    assert engine.get_diff(
        './tests/fixtures/test_nested_old.json',
        './tests/fixtures/test_nested_new.json',
        'plain'
    ) == PLAIN_RESULT_NESTED
