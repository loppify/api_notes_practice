from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.api.tags import router as tags_router
from app.api.tasks import router as tasks_router
from app.api.users import router as users_router
from app.exception_handlers import register_exception_handlers

app = FastAPI(title="My FastAPI Task App", docs_url="/docs")
register_exception_handlers(app)
app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(tags_router)


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")
