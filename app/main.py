from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.api.tasks import router as tasks_router

from app.api.users import router as users_router

app = FastAPI(title="My FastAPI Task App")
app.include_router(tasks_router)
app.include_router(users_router)


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")
