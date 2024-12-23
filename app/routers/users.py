import uuid

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.models.user import User
from app.resources import user_resource
from app.utils.utils import extract_access_token_from_header, verify_custom_jwt

user_router = APIRouter()

@user_router.post(path="", tags=["users"],
    responses={
        201: {"description": "User creation successful"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"},
    },
    description="This endpoint creates a new user with the given details."
)
async def create_user(user: dict, request: Request):
    access_token = extract_access_token_from_header(request)
    user_info = verify_custom_jwt(access_token, profile='user')

    user['UID'] = str(uuid.uuid4())
    user['Email'] = user_info['email']
    user['Name'] = user_info['name']
    user['Pic_URL'] = user_info['picture']

    resource = user_resource.UserResource(config = None)
    result = resource.insert_data(User.model_validate(user))
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        result['UID'] = user['UID']
        result['Email'] = user['Email']
        return JSONResponse(content=result, status_code=201)

@user_router.get(path="", tags=["users"],
    responses={
        200: {"description": "User fetched successfully"},
        404: {"description": "User does not exist"},
        500: {"description": "Database not live"},
    },
    description="This endpoint fetches the user details using their email address."
)
async def get_user(request: Request):
    access_token = extract_access_token_from_header(request)
    user_info = verify_custom_jwt(access_token, profile='user')

    resource = user_resource.UserResource(config = None)
    result = resource.get_by_custom_key('Email', user_info['email'])

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)


@user_router.get(path="/{uid}", tags=["users"],
    responses={
        200: {"description": "User fetched successfully"},
        404: {"description": "User does not exist"},
        500: {"description": "Database not live"},
    },
    description="This endpoint fetches a user by their unique UID."
)
async def get_user_by_id(uid: str, request: Request):
    access_token = extract_access_token_from_header(request)
    verify_custom_jwt(access_token, profile='organiser')

    resource = user_resource.UserResource(config = None)
    result = resource.get_by_key(uid)

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)


@user_router.put(path="", tags=["users"],
    responses={
        200: {"description": "User modification successful"},
        400: {"description": "Corrupt user object passed"},
        500: {"description": "Database not live"}
    },
    description="This endpoint modifies the details of an existing user."
)
async def modify_user(user: User, request: Request):
    access_token = extract_access_token_from_header(request)
    user_info = verify_custom_jwt(access_token, profile='user')

    if not user_info or user_info.get('email') != user.Email:
        return JSONResponse(content={'error': 'Access denied'}, status_code=403)

    resource = user_resource.UserResource(config = None)
    result = resource.modify_data(user)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        result['UID'] = user.UID
        return JSONResponse(content=result, status_code=200)


@user_router.delete(path="", tags=["users"],
    responses={
        204: {"description": "User deletion successful"},
        404: {"description": "User not found"},
        500: {"description": "Database not live"}
    },
    description="This endpoint deletes a user by their email address."
)
async def delete_user(request: Request):
    access_token = extract_access_token_from_header(request)
    user_info = verify_custom_jwt(access_token, profile='user')

    resource = user_resource.UserResource(config = None)
    result = resource.delete_data_by_custom_key('Email', user_info['email'])

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=204)