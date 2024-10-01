from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form
from starlette.responses import JSONResponse

from app.models.organiser import Organiser
from app.resources import organiser_resource
from app.utils.utils import hash_password, authenticate_profile


organiser_router = APIRouter()

@organiser_router.post("/createOrganiser", tags=["organisers"],
    responses={
        200: {"description": "Organiser creation successful"},
        400: {"description": "Corrupt organiser object passed"},
        500: {"description": "Database not live"},
    }
)
async def create_organiser(organiser: Organiser):
    organiser.HashedPswd = hash_password(organiser.HashedPswd)
    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.insert_data(organiser)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)

'''
Below are the actual credentials for organisers. The passwords stored in DB are hashed.

alice.johnson@example.com, ffffffff
david.smith@example.com, gggggggg
sophia.garcia@example.com, hhhhhhhh
liam.thompson@example.com, iiiiiiii
emma.brown@example.com, jjjjjjjj
'''
@organiser_router.post("/authenticate", tags=["organisers"],
    responses={
        200: {"description": "Authorization Successful"},
        401: {"description": "Unauthorized - Incorrect Password"},
        404: {"description": "Organiser not found"},
    }
)
async def authenticate(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.get_by_custom_key("Email", email)

    if result is None:
        return JSONResponse(content={"message": f"{email} not found!"}, status_code = 404)
    elif 'error' in result.keys(): # result is some error
        return JSONResponse(content=result, status_code=500)

    if authenticate_profile(password, result):
        return JSONResponse(content={"message": f"Authorization Successful!, Organiser: {result['Name']}"}, status_code=200)
    else:
        return JSONResponse(content={"message": f"Authorization unsuccessful! Incorrect Password for {email}"}, status_code = 401)
