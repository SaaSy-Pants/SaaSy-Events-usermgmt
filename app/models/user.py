from __future__ import annotations

from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    UID: str = constr(min_length=1, max_length=5)  # Treat as primary key in logic
    Name: str
    Email: EmailStr = constr(min_length=1, max_length=50)
    PhoneNo: str = constr(min_length=1, max_length=15)
    Address: str
    Age: int

    class Config:
        json_schema_extra = {
            "user": {
                "UID": "U001",
                "Name": "John Doe",
                "Email": "johndoe@example.com",
                "PhoneNo": "+1234567890",
                "Address": "123 Main St, City, Country",
                "Age": "30"
            }
        }
        orm_mode = True
