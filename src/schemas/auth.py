from pydantic import BaseModel


class EmailRequest(BaseModel):
    email: str


class VerifyRequest(BaseModel):
    email: str
    code: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    nickname: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str
