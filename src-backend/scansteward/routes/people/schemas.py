from ninja import Schema


class PersonCreateSchema(Schema):
    """
    Schema to create a Person
    """

    name: str
    description: str | None = None


class PersonReadSchema(PersonCreateSchema):
    """
    Schema when reading a person
    """

    id: int


class PersonUpdateSchema(Schema):
    """
    Schema to update a person
    """

    # TODO: Validate one or both fields provided
    name: str | None = None
    description: str | None = None
