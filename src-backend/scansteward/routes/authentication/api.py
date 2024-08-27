import logging
from datetime import timedelta
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from django.utils import timezone
from ninja import Router
from ninja.security import django_auth

from scansteward.common.authentication import AuthApiKey
from scansteward.models import Token
from scansteward.routes.authentication.schemas import TokenCreateInSchema
from scansteward.routes.authentication.schemas import TokenReadOutSchema

router = Router(tags=["auth"])
logger = logging.getLogger(__name__)


@router.post(
    "/token/create/",
    response={HTTPStatus.CREATED: TokenReadOutSchema},
    auth=[django_auth, AuthApiKey()],
)
def create_token(request: HttpRequest, token_data: TokenCreateInSchema):
    token = Token.objects.create(
        user=request.user,
        name=token_data.name,
        expires_at=timezone.now() + timedelta(days=token_data.expires_in_days) if token_data.expires_in_days else None,
    )
    return TokenReadOutSchema(
        key=token.key,
        name=token.name,
        expires_at=token.expires_at,
    )


@router.get("/token/", response=list[TokenReadOutSchema], auth=AuthApiKey())
def list_tokens(request):
    return Token.objects.filter(user=request.auth.user).all()


@router.delete(
    "/tokens/{token_key}",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def revoke_token(request, token_key: str):
    token: Token = await aget_object_or_404(Token, key=token_key, user=request.auth.user)
    await token.adelete()
    return HTTPStatus.NO_CONTENT, None
