from pydantic import BaseModel, Field


class SuccessSchema(BaseModel):
    """The response scheme, if the request was completed successfully."""

    result: bool = Field(
        ...,
        description="The boolean value is whether the request was "
                    "completed successfully or not."
    )


class Error(BaseModel):
    """The schema is an object with a description of the error."""

    result: bool = Field(
        ...,
        description="The boolean value is whether the request was "
                    "completed successfully or not."
    )
    descr: str = Field(
        ...,
        description="A small clarification of what caused the error."
    )


class ErrorSchema(BaseModel):
    """The response scheme if the request ended with some kind of error."""
    detail: Error = Field(
        ...,
        description="An object with errors."
    )


class TokenSchema(BaseModel):
    """The scheme for returning the token."""

    access_token: str = Field(
        ..., description="An authentication token."
    )
    token_type: str = Field(
        ...,
        description="The type will always be Bearer, it also needs to be "
                    "substituted in headers.",
    )


class TokenReset(BaseModel):
    """A scheme for returning the token, for resetting the password."""

    token: str = Field(
        ..., description="A token for authenticating the user when "
                         "the password is reset."
    )
