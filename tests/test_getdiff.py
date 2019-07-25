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


# def test_wrong_formats():

# def test_different_formats():


def test_flat_json_to_string():
    string_result = ('{\n'
        '    constant: yep\n'
        '  - test: bar\n'
        '  + test: foo\n'
        '  - foo: bar\n'
        '  + bar: foo\n'
    '}')
    assert string_result == engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json'
    )


def test_flat_json_to_plain():
    plain_result = (
        'Property "test" was changed. From "bar" to "foo"\n'
        'Property "foo" was removed\n'
        'Property "bar" was added with value: "foo"'
    )
    assert plain_result == engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json',
        'plain'
    )


def test_flat_json_to_json():
    json_result = json.dumps({
        'constant': 'yep',
        '- test': 'bar',
        '+ test': 'foo',
        '- foo': 'bar',
        '+ bar': 'foo'
    })
    assert json_result == engine.get_diff(
        './tests/fixtures/test_flat1.json',
        './tests/fixtures/test_flat2.json',
        'json'
    )