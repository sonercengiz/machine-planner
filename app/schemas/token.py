from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str  # genelde "bearer"


class TokenPayload(BaseModel):
    sub: str          # create_access_token'ta koyduğumuz "subject" (ör. user_id)
    exp: int          # Unix timestamp
