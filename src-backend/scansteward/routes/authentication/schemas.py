from ninja import Field
from ninja import Schema
from pydantic import AwareDatetime


class TokenOutResponse(Schema):
    key: str
    name: str | None = None
    expires_at: AwareDatetime | None = None


class TokenInCreateSchema(Schema):
    name: str | None = None
    expires_in_days: int | None = Field(default=None, gt=0)
