lint:
	black --exclude venv/ --check .

typecheck:
	mypy --exclude venv/ .

pytest:
	pytest --cov=chapter2 --cov=chapter3 --cov=chapter3_project --cov=chapter4 --cov=chapter5 --cov=chapter6 --cov=chapter7 --cov=chapter8 --cov=chapter9 --cov=chapter12 --cov chapter13 --cov chapter14 --cov-report=term-missing

test: lint typecheck pytest

cleanup:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf *.db* .mypy_cache .pytest_cache
