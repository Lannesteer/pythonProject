from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/support")
def get_support_page(request: Request):
    return templates.TemplateResponse("support.html", {"request": request})
