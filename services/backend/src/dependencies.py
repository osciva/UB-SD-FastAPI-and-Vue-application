from functools import lru_cache
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.backend.src import utils
from jose import jwt
from pydantic import ValidationError
# from services.backend.src.schemas import TokenPayload, SystemAccount


@lru_cache()
def get_settings():
    return utils.Settings()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


# async def get_current_user(token: str = Depends(reuseable_oauth),
#                            settings: Annotated[config.Settings, Depends(get_settings)]) -> SystemAccount:
#     try:
#         payload = jwt.decode(
#             token, settings.jwt_secret_key, algorithms=[settings.algorithm]
#         )
#         token_data = TokenPayload(**payload)
#
#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except(jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     username: str = token_data.sub
#     # get user from database
#     # if user does not exist, raise an exception
#     # if user exist, return user Schema with password hashed
#     return SystemAccount(**user)
#
