# Settings
set fallback := true

# Environment Variables
export PYTHONDONTWRITEBYTECODE := "1"

#
# Environments
#
[private]
lint-environment:
  poetry install --only lint --no-root

[private]
main-environment:
  poetry install --only main --no-root

[private]
typing-environment: main-environment
  poetry install --only typing --no-root

[private]
test-environment: main-environment
  poetry install --only test --no-root

#
# Linting
#

lint: lint-environment
  poetry run black .
  poetry run ruff .
  poetry run black .

#
# Typing
#

[no-cd]
check-types: typing-environment
  poetry run mypy --config-file pyproject.toml .

#
# Alembic/migrations
#

make-migrations message: main-environment
  poetry run alembic revision --autogenerate -m "{{message}}"

migrate: main-environment
  poetry run alembic upgrade head

#
# Server
#
run: main-environment
  poetry run litestar --app app.main:app run

test: test-environment
  poetry run pytest

test-cov: test-environment
  poetry run coverage erase
  poetry run pytest --cov --cov-report=json
  poetry run coverage report
  poetry run coverage html
