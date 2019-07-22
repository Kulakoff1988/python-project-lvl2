import pytest

from gendiff.comparison import comparator

def test_default():
    comparator.get_diff({}, {}) == '{\n}'

# def test_flat_json():
#     comparator