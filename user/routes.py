from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from user.schema import *
from user.models import UserModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import settings
import secrets
from auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)

router = APIRouter(tags=["Users"], prefix="/Users")


def generate_token(length=32):
    return secrets.token_hex(length)


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = (
        db.query(UserModel)
        .filter(
            or_(
                UserModel.username == request.username_or_email.lower(),
                UserModel.email == request.username_or_email.lower(),
            )
        )
        .first()
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    response = JSONResponse(content={"detail": "Login successfully"})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/",
    )

    return response


@router.post("/logout")
async def user_logout():
    response = JSONResponse(content={"detail": "Logout successfully"})

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
    )

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
    )

    return response


@router.post("/register")
async def user_register(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already exist",
        )

    if db.query(UserModel).filter_by(email=request.email.lower()).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already exist",
        )
    user_obj = UserModel(
        username=request.username.lower(),
        email=request.email.lower(),
    )

    user_obj.set_password(request.password)

    db.add(user_obj)
    db.commit()

    return JSONResponse(content={"detail": "User registered successfully"})


@router.post("/refresh_token")
async def user_refresh_token(
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )

    user_id = decode_refresh_token(refresh_token)

    user_obj = db.query(UserModel).filter_by(id=user_id).one_or_none()

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed, user not found",
        )

    access_token = generate_access_token(user_id)

    response = JSONResponse(content={"detail": "Access token refreshed successfully"})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/",
    )

    return response
