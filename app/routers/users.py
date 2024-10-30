from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form
from starlette.responses import JSONResponse

from app.models.user import User
from app.resources import user_resource
from app.utils.utils import hash_password, authenticate_profile

user_router = APIRouter()

@user_router.post(path="", tags=["users"],
    responses={
        200: {"description": "User creation successful"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"},
    }
)
async def create_user(user: User):
    user.HashedPswd = hash_password(user.HashedPswd)
    resource = user_resource.UserResource(config = None)
    result = resource.insert_data(user)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)

@user_router.get(path="/{userId}", tags=["users"],
    responses={
        200: {"description": "User fetched successfully"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"},
    }
)
async def get_user(userId: str):
    resource = user_resource.UserResource(config = None)
    result = resource.get_by_key(userId)

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)


'''
Below are the actual credentials for users. The passwords stored in DB are hashed.

johndoe@example.com, aaaaaaaa
janesmith@example.com, bbbbbbbb
robertbrown@example.com, cccccccc
emilydavis@example.com, dddddddd
michaeljohnson@example.com, eeeeeeee
'''
@user_router.post("/authenticate", tags=["users"],
    responses={
        200: {"description": "Authentication Successful"},
        401: {"description": "Unauthenticated - Incorrect Password"},
        404: {"description": "User not found"},
    }
)
async def authenticate(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    resource = user_resource.UserResource(config = None)
    result = resource.get_by_custom_key("Email", email)

    if result is None:
        return JSONResponse(content={"message": f"{email} not found!"}, status_code = 404)
    elif 'error' in result.keys(): # result is some error
        return JSONResponse(content=result, status_code=500)

    if authenticate_profile(password, result):
        return JSONResponse(content={"message": f"Authentication Successful!, User: {result['Name']}"}, status_code=200)
    else:
        return JSONResponse(content={"message": f"Authentication - Unsuccessful! Incorrect Password for {email}"}, status_code = 401)

@user_router.put(path="", tags=["users"],
    responses={
        200: {"description": "User modification successful"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"}
    }
)
async def modify_user(user: User):
    user.HashedPswd = hash_password(user.HashedPswd)
    resource = user_resource.UserResource(config = None)
    result = resource.modify_data(user)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)


@user_router.delete(path="/{userId}", tags=["users"],
    responses={
        200: {"description": "User deletion successful"},
        400: {"description": "User not found"},
        500: {"description": "Database not live"}
    }
)
async def delete_user(userId: str):
    resource = user_resource.UserResource(config = None)
    result = resource.delete_data_by_key(userId)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)