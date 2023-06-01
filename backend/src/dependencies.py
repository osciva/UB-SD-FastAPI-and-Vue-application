# from distutils.command.config import config
# from typing import Union, Any
# from datetime import datetime
# from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic.tools import lru_cache
# from sqlalchemy.sql.functions import user

import utils
# from jose import jwt
# from pydantic import ValidationError
# from backend.schemas import TokenPayload, SystemAccount


@lru_cache()
def get_settings():
    return utils.Settings()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)



