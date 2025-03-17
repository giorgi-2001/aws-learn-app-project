from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from .aws.az_func import get_ec2_metadata_token, get_az_info
from .images_routes import router as image_router
from .templates import templates


app  = FastAPI()


@app.get("/")
def greeting(request: Request):
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

    return templates.TemplateResponse("index.html", context)


app.include_router(router=image_router)
