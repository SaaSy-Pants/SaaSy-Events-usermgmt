from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.models.organiser import Organiser
from app.resources import organiser_resource

organiser_router = APIRouter()

@organiser_router.post(path="", tags=["organisers"],
    responses={
        201: {"description": "Organiser creation successful"},
        400: {"description": "Corrupt organiser object passed"},
        500: {"description": "Database not live"},
    }
)
async def create_organiser(organiser: Organiser):
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
async def get_organiser(organiserId: str):
    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.get_by_key(organiserId)

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
async def modify_organiser(organiser: Organiser):
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
async def delete_organiser(organiserId: str):
    resource = organiser_resource.OrganiserResource(config = None)
    result = resource.delete_data_by_key(organiserId)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=204)