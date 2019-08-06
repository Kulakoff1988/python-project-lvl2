.PHONY: all install lint package_install
all: install
install:
	@poetry install
lint:
	@poetry run flake8 gendiff --count --ignore=F401
package_install:
	@pip install --user --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ kulakoff1988-gendiff
run_diff_yaml:
	@poetry run gendiff tests/fixtures/test1.yml tests/fixtures/test2.yml
	@poetry run gendiff tests/fixtures/test1.yml tests/fixtures/test2.yml -f plain
	@poetry run gendiff tests/fixtures/test1.yml tests/fixtures/test2.yml -f json
run_diff_str:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.json
	@poetry run gendiff tests/fixtures/test1.json tests/fixtures/test2.json
	@poetry run gendiff tests/fixtures/test3.json tests/fixtures/test4.json
run_diff_plain:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.json -f plain
	@poetry run gendiff tests/fixtures/test1.json tests/fixtures/test2.json -f plain
	@poetry run gendiff tests/fixtures/test3.json tests/fixtures/test4.json -f plain
run_diff_json:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.json -f json
	@poetry run gendiff tests/fixtures/test1.json tests/fixtures/test2.json -f json
	@poetry run gendiff tests/fixtures/test3.json tests/fixtures/test4.json -f json
run_diff_error:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.exe
	@poetry run gendiff tests/fixtures/test_flat1.bin tests/fixtures/test_flat2.json
	@poetry run gendiff tests/fixtures/test1.yml tests/fixtures/test_flat2.json

run_test:
	@poetry run pytest -vv
	@poetry run coverage run ./tests/test_getdiff.py