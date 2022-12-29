from fastapi import Response
from app import settings


def _set_access_token_in_response(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        secure=False,
        httponly=True,
        expires=60,
        max_age=60,
    )


def _set_refresh_token_in_response(response: Response, token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        secure=False,
        httponly=True,
        expires=120,
        max_age=120,
    )


class CookieTransport:
    @staticmethod
    def set_tokens_in_response(response, tokens: dict[str, str]) -> None:
        access_token = tokens["access"]
        refresh_token = tokens["refresh"]
        _set_access_token_in_response(response, access_token)
        _set_refresh_token_in_response(response, refresh_token)

    @staticmethod
    def set_access_token_in_response(response: Response, token: str) -> None:
        _set_access_token_in_response(response, token)

    @staticmethod
    def set_refresh_token_in_response(response: Response, token: str) -> None:
        _set_refresh_token_in_response(response, token)
