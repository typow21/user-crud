from typing import Optional
from pydantic import BaseModel, validator, ValidationError
import uuid

class UserRequest(BaseModel):
    first_name: str
    middle_name: Optional[str] = ""
    last_name: str
    email_address: str # unique
    phone_number: str # can be composite

class User(UserRequest):
    id: str = None

    @validator("id", pre=True, always=True)
    def validate_id(cls, value):
        if not value:
            return str(uuid.uuid4())
        try:
            # Convert the string to a UUID object to validate format
            uuid.UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format for id")
        return value

