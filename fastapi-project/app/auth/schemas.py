from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from app.auth.examples import ex_user_create
from app.core.models import UUIDModel


class UserBase(SQLModel):
    email: EmailStr
    first_name: str = Field(max_length=255, nullable=False)
    last_name: str = Field(max_length=255, nullable=True)
    is_active: bool = Field(default=False)
    username: str = Field(
            index=True,
            max_length=255,
            nullable=False,
    )


class UserCreate(UserBase):
    password: str = Field(max_length=255, nullable=False)

    class Config:
        schema_extra = {"example": ex_user_create}


class UserRead(UserBase, UUIDModel):
    ...


class JWTPairSchema(SQLModel):
    refresh: str
    access: str
    claims: dict


class AuthLogin(SQLModel):
    email: EmailStr
    password: str
