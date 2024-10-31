from typing import Optional
from pydantic import BaseModel, validator, ValidationError
import uuid
import re

class UserRequest(BaseModel):
    first_name: str
    middle_name: Optional[str] = ""
    last_name: str
    email_address: str # unique
    phone_number: str # can be composite

    @validator("email_address")
    def validate_unique_email(cls, email):
        # Simple regex pattern for validating emails
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address format")
        
        return email

    @validator("phone_number")
    def validate_phone_number(cls, phone):
        # Example regex for US phone numbers
        phone_pattern = re.compile(r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")
        if not phone_pattern.match(phone):
            raise ValueError("Invalid phone number format.")
        return phone

    class Config:
        orm_mode = True

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

