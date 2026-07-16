from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import Token, UpdatePassword
from app.models import User

from app.dependencies import (
    CurrentUser,
    UserServiceDep,
    get_current_active_superuser,
)
from app.schemas import UserIn, UserOut, UsersList, UserUpdateMe

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersList,
)
def read_users(service: UserServiceDep, skip: int = 0, limit: int = 100):
    users = service.read_users(skip, limit)
    return UsersList(
        users=[UserOut.model_validate(user) for user in users],
        count=len(users),
    )


@router.post("/signup", response_model=UserOut)
async def create_user(user: UserIn, service: UserServiceDep):
    return await service.add(user, router_prefix=router.prefix)


@router.get("/verify-email")
def verify_email(token: str, service: UserServiceDep):
    service.verify_email(token)
    return {"detail": "Email verified successfully"}


@router.post("/login")
def login_user(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
) -> Token:
    return service.token(request_form.username, request_form.password)


@router.get("/me", response_model=UserOut)
def read_current_user(user: CurrentUser):
    return user


@router.patch("/me", response_model=UserOut)
def update_user_me(
    user_update: UserUpdateMe,
    user: CurrentUser,
    service: UserServiceDep,
) -> User:
    return service.update(user, user_update)


@router.get("/me/forgot-password")
def forgot_password(
    current_user: CurrentUser,
    service: UserServiceDep,
):
    token = service.send_reset_password_link(current_user.model_dump())
    return {
        "detail": "Reset password link sent to your email if the account exists",
        "token": token,
    }


@router.post("/me/reset-password")
def reset_user_password(
    token: str,
    body: UpdatePassword,
    service: UserServiceDep,
):
    service.reset_password(token, body.model_dump())
    return {"detail": "Password updated successfully"}