from fastapi import APIRouter
from starlette.requests import Request

from .templates import templates
from .aws.s3_funcs import get_image_metadata, generate_presigned_url


router = APIRouter(prefix="/images")


@router.get("")
def get_image_by_name(name: str, request: Request):
    img = get_image_metadata(name)
    if img:
        img["url"] = generate_presigned_url(name=name)
    context = {
        "request": request,
        "img": img
    }
    return templates.TemplateResponse("detail.html", context)