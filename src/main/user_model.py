from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class User(BaseModel):

    id: str
    first_name: str
    middle_name: Optional[str] = ""
    last_name: str
    email_address: str # unique
    phone_number: str # can be composite

    # TODO add validators