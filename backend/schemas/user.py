from pydantic import BaseModel, EmailStr
from pydantic import Field


class UserData(BaseModel):
    """
    A scheme for sending user data to the server.
    The user is identified by email, as it is
    unique for each user.
    """
    email: EmailStr = Field(..., description="User's email.")
    password: str = Field(
        ..., min_length=4, description="User's password."
    )


class Email(BaseModel):
    email: EmailStr = Field(..., description="User's email.")


class ResetPassword(BaseModel):
    password: str = Field(
        ..., min_length=4, description="The user's new password."
    )
    token: str = Field(
        ..., description="A token for authenticating the user when "
                         "the password is reset."
    )
