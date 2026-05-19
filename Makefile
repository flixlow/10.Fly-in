ARG ?= --input maps/easy/01_linear_path.txt

install:
	uv sync

run:
	uv run -m src $(ARG)

debug: uv run -m gdb src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .venv

lint:
	uv run flake8 src && mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 src && mypy src --strict