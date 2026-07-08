from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from routers import adding, registry

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(registry.router)
app.include_router(adding.router)

@app.get("/")
async def index():
    return RedirectResponse("/registry/employees", status_code=status.HTTP_301_MOVED_PERMANENTLY)
