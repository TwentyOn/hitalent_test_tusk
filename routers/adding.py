from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from dependencies import templates

router = APIRouter(prefix='/employees', tags=['создание сотрудника'])

@router.get("/", response_class=HTMLResponse)
async def get_create_form(request: Request):
    return templates.TemplateResponse(request, 'create.html', context={'home_url': '/registry/employees/'})

@router.post('/create')
async def create_employee(request: Request):
    print(request)
    return {'message': 'da'}