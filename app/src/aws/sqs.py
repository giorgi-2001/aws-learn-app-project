import json

from botocore.exceptions import ClientError, NoCredentialsError

from ..config import boto_session, SQS_URL
from ..models import Image


sqs = boto_session.client("sqs")

sqs_queue_url = SQS_URL


def format_message(image_metadata: dict, img_url: str | None = None):
    message_text = f"Image - {image_metadata["name"]} - was added to Image App"
    message = {
        "message": message_text,
        "img_metadata": image_metadata
    }
    message["img_metadata"]["url"] = img_url

    return json.dumps(message)


def send_message_to_sqs(message: str, image_extension: str):
    try:
        sqs.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=message,
            MessageAttributes={
                'image_extension': {
                    'StringValue': image_extension,
                    'DataType': 'String'
                }
            },
        )
        return "Success"
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None


def poll_messages_from_sqs():
    try:
        response = sqs.receive_message(
            QueueUrl=sqs_queue_url,
            MessageAttributeNames=['*'],
            MaxNumberOfMessages=10
        )
        return response.get("Messages")
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

