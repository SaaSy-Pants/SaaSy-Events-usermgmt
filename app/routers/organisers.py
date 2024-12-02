from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.models.organiser import Organiser
from app.resources import organiser_resource
from app.utils.utils import extract_access_token_from_header, verify_custom_jwt

organiser_router = APIRouter()

@organiser_router.post(path="", tags=["organisers"],
    responses={
        201: {"description": "Organiser creation successful"},
        400: {"description": "Corrupt organiser object passed"},
        500: {"description": "Database not live"},
    }
)
async def create_organiser(organiser: Organiser, request: Request):
    access_token = extract_access_token_from_header(request)
    organiser_info = verify_custom_jwt(access_token, profile='organiser')

    if not organiser_info or organiser_info.get('email') != organiser.Email:
        return JSONResponse(content={'error': 'Access denied'}, status_code=403)

    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.insert_data(organiser)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        result['OID'] = organiser.OID
        return JSONResponse(content=result, status_code=201)

@organiser_router.get(path="", tags=["organisers"],
    responses={
        200: {"description": "Organiser fetched successfully"},
        404: {"description": "Organiser does not exist"},
        500: {"description": "Database not live"},
    }
)
async def get_organiser(request: Request):
    access_token = extract_access_token_from_header(request)
    organiser_info = verify_custom_jwt(access_token, profile='organiser')

    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.get_by_custom_key('Email', organiser_info['email'])

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=200)


@organiser_router.put(path="", tags=["organisers"],
    responses={
        200: {"description": "Organiser modification successful"},
        400: {"description": "Corrupt organiser object passed"},
        500: {"description": "Database not live"}
    }
)
async def modify_organiser(organiser: Organiser, request: Request):
    access_token = extract_access_token_from_header(request)
    organiser_info = verify_custom_jwt(access_token, profile='organiser')

    if not organiser_info or organiser_info.get('email') != organiser.Email:
        return JSONResponse(content={'error': 'Access denied'}, status_code=403)

    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.modify_data(organiser)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        result['OID'] = organiser.OID
        return JSONResponse(content=result, status_code=200)


@organiser_router.delete(path="", tags=["organisers"],
    responses={
        204: {"description": "Organiser deletion successful"},
        404: {"description": "Organiser not found"},
        500: {"description": "Database not live"}
    }
)
async def delete_organiser(request: Request):
    access_token = extract_access_token_from_header(request)
    organiser_info = verify_custom_jwt(access_token, profile='organiser')

    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.delete_data_by_custom_key('Email', organiser_info['email'])

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=204)