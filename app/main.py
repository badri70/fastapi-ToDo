from fastapi import FastAPI
from app.tasks.routers import router as task_router
from app.users.routers import router as user_router

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)