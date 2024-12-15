import strawberry
from app.utils.utils import extract_access_token_from_header, verify_custom_jwt
from app.resources import user_resource
from app.resources import organiser_resource
from typing import Union

@strawberry.type
class ErrorResponse:
    code: int
    message: str

@strawberry.type
class UserType:
    UID: str  # Primary key
    Name: str
    Email: str
    Pic_URL: str
    PhoneNo: str
    Address: str
    Age: int
    type: str = "User"  # Discriminator field for union handling

    @strawberry.field(name="PicURL")
    def pic_url(self) -> str:
        return self.Pic_URL

@strawberry.type
class OrganiserType:
    OID: str  # Primary key
    Name: str
    Email: str
    Pic_URL: str
    PhoneNo: str
    Address: str
    Age: int
    type: str = "Organiser"  # Discriminator field for union handling

    @strawberry.field(name="PicURL")
    def pic_url(self) -> str:
        return self.Pic_URL

def get_resource_by_key(resource_class, key: str, entity_name: str) -> Union[dict, ErrorResponse]:
    """
    Helper function to fetch resource details by key and handle errors consistently.
    """
    resource = resource_class(config=None)
    result = resource.get_by_key(key)

    if result.get("error") is not None:
        status = result.get("status", "unknown error")
        if status == "bad request":
            return ErrorResponse(code=404, message=f"{entity_name} does not exist")
        return ErrorResponse(code=500, message="Database not live")

    details = result.get("details")
    if details:
        return details

    return ErrorResponse(code=404, message=f"{entity_name} details not found")

@strawberry.type
class Query:
    @strawberry.field
    async def get_user_by_id(self, info, uid: str) -> Union[UserType, ErrorResponse]:
        request = info.context["request"]
        access_token = extract_access_token_from_header(request)

        try:
            verify_custom_jwt(access_token, profile="organiser")
        except Exception as e:
            return ErrorResponse(code=401, message="Not Authorized")

        user_data = get_resource_by_key(user_resource.UserResource, uid, "User")
        return UserType(**user_data) if isinstance(user_data, dict) else user_data

    @strawberry.field
    async def get_organiser_by_id(self, info, oid: str) -> Union[OrganiserType, ErrorResponse]:
        request = info.context["request"]
        access_token = extract_access_token_from_header(request)

        try:
            verify_custom_jwt(access_token, profile="user")
        except Exception as e:
            return ErrorResponse(code=401, message="Not Authorized")

        organiser_data = get_resource_by_key(organiser_resource.OrganiserResource, oid, "Organiser")
        return OrganiserType(**organiser_data) if isinstance(organiser_data, dict) else organiser_data

schema = strawberry.Schema(query=Query)
