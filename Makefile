ARG ?= maps/easy/01_linear_path.txt

install:
	uv sync

run:
	uv run __main__.py $(ARG)

debug: uv run -m gdb src

clean: __pycache__ .mypy_cache

lint: uv run flake8 src and mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: flake8 src and mypy src --strict