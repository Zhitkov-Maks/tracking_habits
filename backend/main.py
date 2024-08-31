from fastapi import FastAPI

from config import settings
from routes.habits import habits_router
from routes.tracking import track_rout
from routes.user import user_rout


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
app.include_router(track_rout)
