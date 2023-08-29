from rest_framework.authentication import TokenAuthentication as DefaultTokenAuthentication

from core.models import Token


class TokenAuthentication(DefaultTokenAuthentication):
    model = Token
