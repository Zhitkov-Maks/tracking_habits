from fastapi import FastAPI

from config import settings
from routes.habits import habits_router
from routes.remind import remind
from routes.tracking import track_rout
from routes.user import user_rout


app = FastAPI(
    root_path=settings.api_v1_prefix,
    title="TRACING HABITS APP",
    description="An API for tracking habits, which helps to instill "
                "new healthy habits.",
    version="1.1.1",
    contact={"name": "Maksim Zhitkov", "email": "m-zhitkov@inbox.ru"},
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(user_rout)
app.include_router(habits_router)
app.include_router(track_rout)
app.include_router(remind)
