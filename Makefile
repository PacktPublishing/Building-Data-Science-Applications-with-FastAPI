lint:
	black --exclude venv/ --check .

typecheck:
	mypy --exclude venv/ .

test: lint typecheck
	pytest --cov=chapter2 --cov=chapter3 --cov-report=term-missing
