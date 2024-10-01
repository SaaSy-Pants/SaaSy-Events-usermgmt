import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(users.user_router, prefix='/users')


@app.get("/")
async def root():
    return {"message": "Hello from the User Management Microservice!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)