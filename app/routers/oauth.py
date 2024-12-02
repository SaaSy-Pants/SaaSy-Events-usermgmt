import os
from http import HTTPStatus
from typing import Annotated

import requests
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import Request, APIRouter, HTTPException
from fastapi.params import Form
from starlette.responses import JSONResponse

from app.resources import user_resource, organiser_resource
from app.utils.constants import GOOGLE_AUTH_URL, GOOGLE_TOKEN_URL, GOOGLE_CERTS_URL
from app.utils.utils import verify_google_access_token, generate_custom_jwt

load_dotenv()


oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    authorize_url=GOOGLE_AUTH_URL,
    authorize_params={'access_type': 'offline', 'prompt': 'consent'},
    access_token_url=GOOGLE_TOKEN_URL,
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri=GOOGLE_CERTS_URL
)


oauth_router = APIRouter()

@oauth_router.get(path = "")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    query_params = request.query_params

    if query_params and (query_params.get('profile') and query_params['profile'].lower() == 'user' or query_params['profile'].lower() == 'organiser'):
        redirect_uri_with_profile = f"{redirect_uri}?{query_params}"
    else:
        return JSONResponse(status_code=400, content={'error': 'Missing or invalid query params'})

    return await oauth.google.authorize_redirect(request, redirect_uri_with_profile)


@oauth_router.route("/auth/callback")
async def auth_callback(request: Request):
    profile = request.query_params.get('profile')
    response = await oauth.google.authorize_access_token(request)

    if not response['id_token']:
        raise HTTPException(status_code=400, detail="OAuth token is missing in the token response.")

    user_info = response['userinfo']
    refresh_token = response['refresh_token']

    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    if not email or not name or not picture:
        raise HTTPException(status_code=400, detail="Missing details in the user info.")

    jwt_token = generate_custom_jwt({'email': email, 'name': name, 'picture': picture}, profile)

    #TODO: Redirect the response to the dashboard link with access token and refresh token as fragment identifiers once UI is hosted
    #return RedirectResponse(f'http://frontend.com/dashboard#access_token={jwt_token}#refresh_token={refresh_token}')

    return JSONResponse(status_code=HTTPStatus.OK, content={"access_token": jwt_token, 'refresh_token': refresh_token})


@oauth_router.post("/refreshToken")
async def refresh_access_token(refresh_token: Annotated[str, Form()], request: Request):
    url = GOOGLE_TOKEN_URL
    data = {
        'client_id': os.getenv('OAUTH_CLIENT_ID'),
        'client_secret': os.getenv('OAUTH_CLIENT_SECRET'),
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    profile = request.query_params.get('profile')
    if not profile or (profile.lower() != 'user' and profile.lower() != 'organiser'):
        return JSONResponse(status_code=400, content={'error': 'Missing or invalid query params'})

    response = requests.post(url, data=data)
    if response.status_code == 200:
        user_info = verify_google_access_token(response.json().get('id_token'))

        # Verifying the user profile
        if profile == 'user':
            resource = user_resource.UserResource(config=None)
            result = resource.get_by_custom_key("Email", user_info.get('email'))
            if not result or not result.get('details'):
                jwt_token = generate_custom_jwt(user_info, 'organiser')
            else:
                jwt_token = generate_custom_jwt(user_info, 'user')
        else:
            resource = organiser_resource.OrganiserResource(config=None)
            result = resource.get_by_custom_key("Email", user_info.get('email'))
            if not result or not result.get('details'):
                jwt_token = generate_custom_jwt(user_info, 'user')
            else:
                jwt_token = generate_custom_jwt(user_info, 'organiser')

        return JSONResponse(status_code=HTTPStatus.OK, content={"access_token": jwt_token})
    else:
        raise Exception(f"Failed to refresh token: {response.json().get('error')}")