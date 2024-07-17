from typing import Annotated

from ninja import Schema
from pydantic import BeforeValidator

CommaToStrList = Annotated[
    list[str],
    BeforeValidator(lambda x: x.split(",")),
]


class BasicFilterSchema(Schema):
    ids: CommaToStrList | None = None
