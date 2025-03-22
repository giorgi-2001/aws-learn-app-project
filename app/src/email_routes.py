from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from .templates import templates
from .aws.sns import (
    list_sns_subscriptions,
    subscribe_to_sns_topic,
    delete_sns_subscription
) 


router = APIRouter(prefix="/email")


@router.get("")
def email_subscription_page(request: Request):
    context = {"request": request}
    subs = list_sns_subscriptions()
    if subs:
        context["subs"] = subs
    return templates.TemplateResponse("email.html", context)


@router.post("")
def subscribe_new_email(request: Request, email: str = Form(...)):
    subscribe_to_sns_topic(email)
    url = request.url_for("email_subscription_page")
    return RedirectResponse(url, status_code=303)


@router.post("/{arn}/unsubscribe")
def unsubscribe_email(arn: str, request: Request):
    delete_sns_subscription(arn=arn)
    url = request.url_for("email_subscription_page")
    return RedirectResponse(url, status_code=303)