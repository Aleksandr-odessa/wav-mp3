from pydantic import BaseModel, validator, Field
from pydantic.validators import UUID


class Name(BaseModel):
    name: str = Field(..., max_length=10)

    @validator('name')
    def name_not_spec_symbols(cls, names):
        if not names.isalnum():
            raise ValueError('must by only letters numbers. Not spec.symbols')
        return names.title()


class UserData(BaseModel):
    user_id: str
    access_token: int | str | UUID
