import os
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from jose import JWTError, jwt
import boto3
from typing import Optional


import uuid
from datetime import datetime, timezone


from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


router = APIRouter()

CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")

client = boto3.client("cognito-idp", region_name=os.getenv("COGNITO_REGION"))


class SignUpBody(BaseModel):
    username: str
    password: str
    email: str


@router.post("/auth/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(body: SignUpBody):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=body.email,
            Password=body.password,
            UserAttributes=[
                {"Name": "username", "Value": body.username},
                {"Name": "email", "Value": body.email},
            ],
        )
        return {"message": "User registered successfully"}
    except client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class VerificationBody(BaseModel):
    email: str
    code: str


@router.post("/auth/email-verification", status_code=status.HTTP_200_OK)
async def email_verification(body: VerificationBody):
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID, Username=body.email, ConfirmationCode=body.code
        )
        return {"message": "Email verified succesfully"}
    except client.exceptions.CodeMismatchException:
        raise HTTPException(status_code=400, detail="Invalid confirmation code")
    except client.exceptions.ExpiredCodeException:
        raise HTTPException(status_code=400, detail="Confirmation code has expired")
    except client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=400, detail="User not found")


class SignInBody(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str


@router.post("/auth/sign-in", response_model=Token, status_code=status.HTTP_200_OK)
async def sign_in(body: SignInBody):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": body.email, "PASSWORD": body.password},
        )
        return {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
        }

    except client.exceptions.NotAuthorizedException as e:
        raise HTTPException(status_code=400, detail="Invalid username or password")


class RefreshTokenBody(BaseModel):
    refresh_token: str


@router.post("/auth/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(body: RefreshTokenBody):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": body.refresh_token},
        )
        return {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "refresh_token": body.refresh_token,
            "id_token": response["AuthenticationResult"]["IdToken"],
        }
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
