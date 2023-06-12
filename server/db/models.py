from pydantic import BaseModel, Field, validator
from pydantic.validators import UUID


class Name(BaseModel):
    name: str = Field(..., max_length=10)

    @validator('name')
    def name_not_spec_symbols(cls, name:str):
        if not name.isalnum():
            raise ValueError('Please use only letters (a-z, а-я) and numbers')
        return name.title()


class UserData(BaseModel):
    user_id: str
    access_token: int | str | UUID