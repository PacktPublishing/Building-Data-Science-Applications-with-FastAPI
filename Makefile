lint:
	black --exclude venv/ --check .

typecheck:
	mypy --exclude venv/ .

pytest:
	pytest --cov=chapter2 --cov=chapter3 --cov=chapter4 --cov=chapter5 --cov-report=term-missing

test: lint typecheck pytest
