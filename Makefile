.PHONY: all install lint package_install
all: install
install:
	@python3 -m poetry install
lint:
	@python3 -m poetry run flake8 gendiff --count
package_install:
	@pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.test.org/simple/ kulakoff1988-gendiff
run_diff_str:
	@poetry run gendiff tests/test_cases/test_flat1.json tests/test_cases/test_flat2.json
run_diff_plain:
	@poetry run gendiff tests/test_cases/test_flat1.json tests/test_cases/test_flat2.json -f plain
run_diff_json:
	@poetry run gendiff tests/test_cases/test_flat1.json tests/test_cases/test_flat2.json -f json
run_test:
	@poetry run pytest -vv