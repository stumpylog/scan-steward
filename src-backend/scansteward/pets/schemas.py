from ninja import Schema


class PetCreateSchema(Schema):
    """
    Schema to create a Pet
    """

    name: str
    description: str | None = None


class PetReadSchema(PetCreateSchema):
    """
    Schema when reading a pet
    """

    id: int


class PetUpdateSchema(Schema):
    """
    Schema to update a pet
    """

    # TODO: Validate one or both fields provided
    name: str | None = None
    description: str | None = None
