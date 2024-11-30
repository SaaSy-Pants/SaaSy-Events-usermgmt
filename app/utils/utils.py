import os
from datetime import datetime, timedelta

import jwt
import requests
from fastapi import HTTPException, Request
from authlib.jose import jwt as jose_awt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.utils.constants import GOOGLE_CERTS_URL, ALGORITHM


def extract_access_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header is missing or invalid")

    return auth_header.split(" ")[1]


def verify_google_access_token(access_token):
    try:
        jwks_url = GOOGLE_CERTS_URL
        jwks = requests.get(jwks_url).json()
        headers = jwt.get_unverified_header(access_token)
        rsa_key = {}

        for key in jwks['keys']:
            if key['kid'] == headers['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if not rsa_key:
            raise HTTPException(status_code=400, detail="Unable to find appropriate key.")

        payload = jose_awt.decode(access_token, rsa_key)

        user_info = {
            "email": payload.get('email'),
        }

        if not user_info['email']:
            raise HTTPException(status_code=400, detail="Missing email in the ID token.")

        return user_info

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="ID token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error decoding ID token: " + str(e))


def generate_custom_jwt(user_info, profile):
    jwt_claims = {
        **user_info,
        "profile": profile
    }

    expiration_time = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(
        payload={
            **jwt_claims,
            "exp": expiration_time,
            "iat": datetime.utcnow()
        },
        key=os.getenv('JWT_SECRET_KEY'),
        algorithm=ALGORITHM
    )


def verify_custom_jwt(token, profile):
    try:
        decoded_token = jwt.decode(
            token,
            key=os.getenv('JWT_SECRET_KEY'),
            algorithms=[ALGORITHM]
        )
        if decoded_token.get('profile') != profile:
            raise HTTPException(status_code=403, detail="Access denied.")

        return decoded_token

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The auth token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="The auth token is invalid")
