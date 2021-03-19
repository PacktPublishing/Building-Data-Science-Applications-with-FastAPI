lint:
	black --exclude venv/ --check .

typecheck:
	mypy --exclude venv/ .

test: lint typecheck
	pytest
