.PHONY: all install lint package_install
all: install
install:
	@poetry install
lint:
	@poetry run flake8 gendiff --count --ignore=F401
package_install:
	@pip install --user --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ kulakoff1988-gendiff
run_diff_yaml:
	@poetry run gendiff tests/fixtures/test_flat_old.yml tests/fixtures/test_flat_new.yml
	@poetry run gendiff tests/fixtures/test_flat_old.yml tests/fixtures/test_flat_new.yml -f plain
	@poetry run gendiff tests/fixtures/test_flat_old.yml tests/fixtures/test_flat_new.yml -f json
run_diff_str:
	@poetry run gendiff tests/fixtures/test_flat_old.json tests/fixtures/test_flat_new.json
	@poetry run gendiff tests/fixtures/test_nested_old.json tests/fixtures/test_nested_new.json
run_diff_plain:
	@poetry run gendiff tests/fixtures/test_flat_old.json tests/fixtures/test_flat_new.json -f plain
	@poetry run gendiff tests/fixtures/test_nested_old.json tests/fixtures/test_nested_new.json -f plain
run_diff_json:
	@poetry run gendiff tests/fixtures/test_flat_old.json tests/fixtures/test_flat_new.json -f json
	@poetry run gendiff tests/fixtures/test_nested_old.json tests/fixtures/test_nested_new.json -f json
run_diff_error:
	@poetry run gendiff tests/fixtures/test_flat_old.json tests/fixtures/test_flat_new.exe
	@poetry run gendiff tests/fixtures/test_flat_old.bin tests/fixtures/test_flat_new.json
run_test:
	@poetry run pytest -vv
	@poetry run coverage run ./tests/test_getdiff.py