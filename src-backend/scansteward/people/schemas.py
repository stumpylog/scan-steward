from ninja import Schema


class PersonCreate(Schema):
    """
    Schema to create a Person
    """

    name: str
    description: str | None = None


class PersonRead(PersonCreate):
    """
    Schema when reading a person
    """

    id: int


class PersonUpdate(Schema):
    """
    Schema to update a person
    """

    # TODO: Validate one or both fields provided
    name: str | None = None
    description: str | None = None
