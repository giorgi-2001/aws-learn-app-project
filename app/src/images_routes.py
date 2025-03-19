from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, Query
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from .templates import templates
from .aws.s3_funcs import (
    get_image_metadata,
    generate_presigned_url,
    upload_image_to_s3,
    delete_image_from_s3
)
from .modelDAO import ImageDAO
from .schemas import QueryParams


router = APIRouter(prefix="/images")


db_dependency = Annotated[ImageDAO, Depends(ImageDAO)]


@router.get("/")
async def get_all_images(
    request: Request, db: db_dependency, filters: QueryParams = Depends()
):
    context = {"request": request}
    images = await db.get_all_images(**filters.model_dump())
    context["images"] = images
    return templates.TemplateResponse("image-list.html", context)


@router.get("/{name}")
async def get_image_by_name(name: str, request: Request, db: db_dependency):
    context = {"request": request,}
    img = await db.get_image_by_name(name)

    if not img:
        return templates.TemplateResponse("404.html", context)
    
    image_data = {
        "url": generate_presigned_url(name=name),
        "name": name,
        "size": img.size,
        "extension": img.extension,
        "last_update": img.updated_at.strftime("%b %d %Y, %I:%M%p")
    }
    context["img"] = image_data
    return templates.TemplateResponse("detail.html", context)


@router.post("/upload")
async def upload_image(
    db: db_dependency, 
    request: Request, file: UploadFile = File(...)
):
    name = file.filename
    content = await file.read()
    await file.close()

    upload_image_to_s3(name, content)
    img_metadata = get_image_metadata(name)

    img_exists_in_db = await db.get_image_by_name(name)

    if img_exists_in_db:
        await db.update_image(img_metadata)
    else:
        await db.save_image(img_metadata)
 
    url = request.url_for("get_image_by_name", name=name)
    return RedirectResponse(url, status_code=303)


@router.post("/{name}/delete")
async def delete_image(name: str, db: db_dependency, request: Request):
    img_exists = await db.get_image_by_name(name)
    if img_exists:
        delete_image_from_s3(name)
        await db.delete_image(name)
    url = request.url_for("get_all_images")
    return RedirectResponse(url, status_code=303)