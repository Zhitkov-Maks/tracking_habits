from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.responses import JSONResponse

from config import settings
from routes.habits import habits_router
from routes.remind import remind
from routes.tracking import track_rout
from routes.user import user_rout
from routes.comment import comment_rout
from crud.user import cleanup_expired_tokens


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
app.include_router(comment_rout)


@app.get("/health")
async def health_check() -> JSONResponse:
    """It is needed to inform about readiness for work."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "tracking_app"}
    )


scheduler = BackgroundScheduler()


async def scheduled_cleanup():
    async with AsyncSession() as session:
        await cleanup_expired_tokens(session)


scheduler.add_job(scheduled_cleanup, 'interval', days=1)
scheduler.start()
