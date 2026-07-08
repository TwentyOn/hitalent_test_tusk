from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from dependencies import templates

router = APIRouter(prefix="/registry", tags=["реестр"])

@router.get("/employees", response_class=HTMLResponse)
async def view(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "employees":
             [
                 {'name': 'Ерещенко Алексей Геннадьевич', 'age': 27, 'sex': 'Муж', 'phone': '7-800-555-35-35'}
             ],
            'create_url': '/employees/'}
    )