from django.http import HttpRequest
from ninja.security import APIKeyHeader

from scansteward.models import Token


class AuthApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: str):
        try:
            token_obj = Token.objects.get(key=key)
            if token_obj.is_valid():
                token_obj.update_last_used()
                return token_obj
        except Token.DoesNotExist:
            pass
        return None
