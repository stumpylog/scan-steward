from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from app.models.others import Person


class PersonRepository(SQLAlchemyAsyncRepository[Person]):
    """
    Person repository
    """

    model_type = Person
