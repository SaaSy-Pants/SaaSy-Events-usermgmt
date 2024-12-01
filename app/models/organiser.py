from __future__ import annotations

from pydantic import BaseModel, constr, EmailStr


class Organiser(BaseModel):
    OID: str = constr(min_length=1, max_length=5)  # Treat as primary key in logic
    Name: str
    Email: EmailStr = constr(min_length=1, max_length=50)
    PhoneNo: str = constr(min_length=1, max_length=15)
    Address: str
    Age: int

    class Config:
        json_schema_extra = {
            "organiser": {
                "UID": "O001",
                "Name": "Alice Johnson",
                "Email": "alice.johnson@example.com",
                "PhoneNo": "+1987654321",
                "Address": "789 Maple Ave, Cityville, Country",
                "Age": "28"
            }
        }
        orm_mode = True
