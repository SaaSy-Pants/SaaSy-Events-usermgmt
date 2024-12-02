import secrets

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers import users, organisers, health, oauth
from app.middleware.logging import LoggingMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Logging Middleware
app.add_middleware(LoggingMiddleware)

#Session Middleware
secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

app.include_router(users.user_router, prefix='/user')

app.include_router(organisers.organiser_router, prefix='/organiser')

app.include_router(health.health_router, prefix='/health')

app.include_router(oauth.oauth_router, prefix='/login')

@app.get("/")
async def root():
    return {"message": "Hello from the User Management Microservice!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
