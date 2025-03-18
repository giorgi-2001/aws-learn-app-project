import random
from typing import Annotated

from fastapi import FastAPI, Depends
from starlette.requests import Request

from .aws.az_func import get_ec2_metadata_token, get_az_info
from .images_routes import router as image_router
from .templates import templates
from .modelDAO import ImageDAO


app  = FastAPI()


db_dependency = Annotated[ImageDAO, Depends(ImageDAO)]


@app.get("/")
async def greeting(request: Request, db: db_dependency):
    reg_info = {}
    token = get_ec2_metadata_token()

    if token:
        availability_zone = get_az_info(token)
        region = availability_zone[:-1]
        reg_info.update({
            "region": region,
            "az": availability_zone
        })

    context = {
        "request": request,
        "reg_info": reg_info
    }

    images = await db.get_all_images()

    if images:
        random_image = random.choice(images)
        context["rand_img_name"] = random_image.name

    return templates.TemplateResponse("index.html", context)


app.include_router(router=image_router)
