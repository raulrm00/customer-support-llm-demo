from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """JWT payload content."""
    sub: str | None = None
