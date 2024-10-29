import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, organisers, health
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

app.include_router(users.user_router, prefix='/user')

app.include_router(organisers.organiser_router, prefix='/organiser')

app.include_router(health.health_router, prefix='/health')

@app.get("/")
async def root():
    return {"message": "Hello from the User Management Microservice!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
