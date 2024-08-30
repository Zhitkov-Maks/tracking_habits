from fastapi import FastAPI
from starlette import status

from config import settings
from routes.habits import habits_router
from routes.user import user_rout
from schemas.user import ReturnUserSchema


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "tweets",
        "description": "Manage tweets.",
    },
    {"name": "images", "description": "Operations with images"},
]


app = FastAPI(
    root_path=settings.api_v1_prefix,
    title="TRACING HABITS APP",
    description="API for tracking habits, helps to develop new "
                "habits and remove destructive ones.",
    version="0.0.1",
    contact={
        "name": "Maksim Zhitkov",
        "email": "m-zhitkov@inbox.ru"
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.include_router(user_rout)
app.include_router(habits_router)


@app.get(
    "/user",
    status_code=status.HTTP_200_OK,
    response_model=ReturnUserSchema,
    tags=["users"]
)
async def simple_get_data():
    return {
        "response": True,
        "data": {
            "username": "Maksim",
            "password": "Zhitkov123",
            "user_chat_id": 123789
        }
    }
