# Environment Variables
export PYTHONDONTWRITEBYTECODE := "1"

# Default Arguments
default_docs_port := '8000'

#
# Clean
#
clean:
  echo "Cleaning working directory"
  fd --hidden --glob '*.pyc' --type file --exec rm .
  fd --hidden --glob '*.pyo' --type file --exec rm .
  fd --hidden --glob '__pycache__' --type directory --exec rm -r .
  fd --hidden --glob '.pytest_cache' --type directory --exec rm -r .
  fd --hidden --glob '.mypy_cache' --type directory --exec rm -r .
  fd --hidden --glob '.ruff_cache' --type directory --exec rm -r .

#
# Documentation
#

[private]
docs-environment:
  poetry install --only docs --no-root

build-docs: docs-environment
  poetry run mkdocs build

serve-docs port=default_docs_port: docs-environment
  poetry run mkdocs serve --dev-addr "localhost:{{port}}"

#
# Testing
#

[private]
test-environment:
  poetry install --with test

[no-cd]
test: test-environment
  poetry run pytest

[no-cd]
test-cov: test-environment
  poetry run pytest --cov

#
# Linting
#

[private]
lint-environment:
  poetry install --only lint --no-root

[no-cd]
lint: lint-environment
  poetry run black .
  poetry run ruff .
  poetry run black .

#
# Type Checking
#

[private]
typing-environment:
  poetry install --only typing --no-root

[no-cd]
check-types: typing-environment
  poetry run mypy --install-types --config-file ../pyproject.toml .

#
# API
#

[private]
main-environment:
  poetry install --only main --no-root

[no-cd]
server: main-environment
  #poetry.exe run granian --reload --interface asgi --no-ws scansteward.asgi:application
  poetry.exe run hypercorn --reload scansteward.asgi:application
