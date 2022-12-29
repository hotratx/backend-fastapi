from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi import status as http_status

from app.core.models import StatusMessage
from app.auth.crud import AuthCRUD
from app.auth.dependencies import get_auth_crud, get_authenticated_user
from app.auth.schemas import UserCreate, UserBase, JWTPairSchema, AuthLogin
from app.auth.authentication import AuthService
from app.auth.transport import CookieTransport

router = APIRouter()


@router.get(
    "/me",
    response_model=UserBase,
)
async def me(user: dict = Depends(get_authenticated_user)):
    """
    Verify if request is authenticated
    """
    # return {"Authenticated": user.is_authenticated, "username": user.username}
    return user


@router.post(
    "/register",
    response_model=UserBase,
    status_code=http_status.HTTP_201_CREATED
)
async def register(
        response: Response,
        data: UserCreate,
        service: AuthService = Depends(AuthService)
):
    tokens, user = await service.register(data)
    return user


@router.post(
    "/login",
    response_model=JWTPairSchema,
    status_code=http_status.HTTP_200_OK
)
async def login(
        response: Response,
        request: Request,
        data: AuthLogin,
        service: AuthService = Depends(AuthService)
):
    ip = request.client.host
    tokens = await service.login(data=data, ip=ip)
    CookieTransport.set_tokens_in_response(response, tokens)
    return tokens


@router.get("/refresh-token")
async def refresh_access_token(
    request: Request,
    response: Response,
    service: AuthService = Depends(AuthService),
):
    """
    refresh an access token

    Args:
        request (Request): Request
        response (Response): Response

    Raises:
        HTTPException: HTTPException

    Returns:
        Response
    """
    refresh_token = request.cookies.get("refresh")
    if refresh_token is None:
        raise HTTPException(401)

    access_token = await service.refresh_access_token(refresh_token)
    CookieTransport.set_access_token_in_response(response, access_token)
    return {"access": access_token}


@router.get(
    "/{user_id}",
    response_model=UserBase,
    status_code=http_status.HTTP_200_OK
)
async def get_user_by_uuid(
        user_id: str,
        users: AuthCRUD = Depends(get_auth_crud)
):
    user = await users.get(user_id=user_id)

    return user


@router.delete(
    "/{user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_user_by_uuid(
        user_id: str,
        users: AuthCRUD = Depends(get_auth_crud)
):
    status = await users.delete(user_id=user_id)

    return {"status": status, "message": "The user has been deleted!"}
