ARG ?=
LINT_FLAG = --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

run: install
	uv run main.py $(ARG)

install: map
	uv sync

debug:
	uv run -m pdb main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .venv
	rm -rf maps

lint: install
	uv run flake8 . --exclude .venv 
	uv run mypy . --exclude .venv $(LINT_FLAG)

lint-strict: install
	uv run flake8 . --exclude .venv
	uv run mypy . --exclude .venv --strict

map: maps/.installed

maps/.installed: data/maps.tar.gz
	tar -xf data/maps.tar.gz
	touch maps/.installed

.PHONY: run install debug clean lint lint-strict map