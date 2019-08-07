[![Build Status](https://travis-ci.com/Kulakoff1988/python-project-lvl2.svg?branch=master)](https://travis-ci.com/Kulakoff1988/python-project-lvl2)
[![Maintainability](https://api.codeclimate.com/v1/badges/277adc00cbc4dfb33d09/maintainability)](https://codeclimate.com/github/Kulakoff1988/python-project-lvl2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/277adc00cbc4dfb33d09/test_coverage)](https://codeclimate.com/github/Kulakoff1988/python-project-lvl2/test_coverage)

# Diff generator

This is the utility for getting diff between two json or yaml files.

Bellow you may see the way to install and use the package:
```
pip install --user --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ kulakoff1988-gendiff
```
[![asciicast](https://asciinema.org/a/259941.svg)](https://asciinema.org/a/259941)

To get diff between two flat yaml or json files use the command:
```
gendiff tests/fixtures/test1.yml tests/fixtures/test2.yml
```
The output in the string format by default:
```
{
    constant: yep
  - test: bar
  + test: foo
  - foo: bar
  + bar: foo
}
```
[![asciicast](https://asciinema.org/a/259968.svg)](https://asciinema.org/a/259968)

To get diff between two recursive structure files use next:
```
gendiff tests/fixtures/test1.json tests/fixtures/test2.json
```
Output:
```
{
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
}
```
[![asciicast](https://asciinema.org/a/259969.svg)](https://asciinema.org/a/259969)

To get diff between two files in plain format use the command:
```
gendiff tests/fixtures/test1.json tests/fixtures/test2.json -f plain
```
```
Property "common.setting2" was removed
Property "common.setting6" was removed
Property "common.setting4" was added with value: "blah blah"
Property "common.setting5" was added with value: "complex value"
Property "group1.baz" was changed. From "bas" to "bars"
Property "group2" was removed
Property "group3" was added with value: "complex value"
```
[![asciicast](https://asciinema.org/a/259970.svg)](https://asciinema.org/a/259970)

To get diff between two files in json format use the command:
[![asciicast](https://asciinema.org/a/259972.svg)](https://asciinema.org/a/259972)
