.PHONY: all install lint package_install
all: install
install:
	@python3 -m poetry install
lint:
	@python3 -m poetry run flake8 gendiff --count
package_install:
	@pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.test.org/simple/ kulakoff1988-gendiff
run_diff_str:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.json
run_diff_plain:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.json -f plain
run_diff_json:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.json -f json
run_diff_error:
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.exe
	@poetry run gendiff tests/fixtures/test_flat1.exe tests/fixtures/test_flat2.json
	@poetry run gendiff tests/fixtures/test_flat1.json tests/fixtures/test_flat2.yml
run_test:
	@poetry run pytest -vv