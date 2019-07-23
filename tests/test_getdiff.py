import pytest
import json
from gendiff.comparison import comparator

def test_empty():
    assert None == comparator.get_diff(
        './tests/test_cases/test_empty1.json',
        './tests/test_cases/test_empty2.json'
    )


def test_flat_json():
    string_result = ('{\n'
        '    constant: yep\n'
        '  - test: bar\n'
        '  + test: foo\n'
        '  - foo: bar\n'
        '  + bar: foo\n'
    '}')
    plain_result = (
        'Property "test" was changed.From "bar" to "foo"\n'
        'Property "foo" was removed\n'
        'Property "bar" was added with value: "foo"'
    )
    json_result = {
        "constant": "yep",
        "- test": "bar",
        "+ test": "foo",
        "- foo": "bar",
        "+ bar": "foo"
    }
    assert string_result == comparator.get_diff(
        './tests/test_cases/test_flat1.json',
        './tests/test_cases/test_flat2.json'
    )
    assert plain_result == comparator.get_diff(
        './tests/test_cases/test_flat1.json',
        './tests/test_cases/test_flat2.json',
        'plain'
    )
    # assert json_result == comparator.get_diff(
    #     './tests/test_cases/test_flat1.json',
    #     './tests/test_cases/test_flat2.json',
    #     'json'
    # )