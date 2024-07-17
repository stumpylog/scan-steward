import enum


@enum.unique
class DatabaseChoices(enum.Enum):
    Sqlite3 = "sqlite3"
    Postgres = "postgres"
    MariaDB = "mariadb"
