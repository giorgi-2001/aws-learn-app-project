from fastapi import APIRouter
from starlette.requests import Request

from .templates import templates
from .images_routes import db_dependency
from .aws.lambda_func import invoke_lambda


router = APIRouter(prefix="/data")


@router.get("")
async def check_data_consistency(request: Request, db: db_dependency):
    context = {"request": request}
    images = await db.get_all_images()
    img_names = [img.name for img in images]
    response = invoke_lambda(data={"Records": img_names})
    print("Type of Response: ", type(response))
    context.update(response)
    return templates.TemplateResponse("data.html", context=context)
