ARG ?=

run: install
	uv run python3 -m src $(ARG)

install: map
	uv sync

debug:
	uv run -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .venv
	rm -rf maps

lint:
	uv run flake8 src && uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src && uv run mypy src --strict

map: maps/.installed

maps/.installed: data/maps.tar.gz
	tar -xf data/maps.tar.gz
	touch maps/.installed

.PHONY: run install debug clean lint lint-strict map