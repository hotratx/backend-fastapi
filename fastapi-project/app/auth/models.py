from sqlmodel import SQLModel
from app.core.models import TimestampModel, UUIDModel
from app.auth.schemas import UserBase

prefix = "usr"


class User(
        TimestampModel,
        UUIDModel,
        UserBase,
        SQLModel,
        table=True
):
    is_superuser: bool = False
    hashed_password: str

    __tablename__ = f"{prefix}_users"
