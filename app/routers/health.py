from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.resources.organiser_resource import OrganiserResource
from app.resources.user_resource import UserResource
from app.services.service_factory import ServiceFactory


health_router = APIRouter()

@health_router.get("/users", tags=["health"])
async def health_check_users():
    # Get the database service
    data_service = ServiceFactory.get_service("UserResourceDataService")
    user_resource = UserResource(config = None)

    # Test database connection
    try:
        result = data_service.check_connection(user_resource.database, user_resource.collection)
        if result['status'] == 'failed':
            return JSONResponse(content=result, status_code=500)
        else:
            return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content = {'status': 'connection failed', 'message': str(e)}, status_code=500)


@health_router.get("/organisers", tags=["health"])
async def health_check_organisers():
    # Get the database service
    data_service = ServiceFactory.get_service("UserResourceDataService")
    organiser_resource = OrganiserResource(config = None)

    # Test database connection
    try:
        result = data_service.check_connection(organiser_resource.database, organiser_resource.collection)
        if result['status'] == 'failed':
            return JSONResponse(content=result, status_code=500)
        else:
            return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content = {'status': 'connection failed', 'message': str(e)}, status_code=500)
