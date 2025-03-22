import json

from botocore.exceptions import ClientError, NoCredentialsError

from ..config import boto_session, SNS_TOPIC_ARN


sns = boto_session.client("sns")

topic = SNS_TOPIC_ARN

email_template = """
Hello dear, Image App user
We are notifying you about recent changes regarding the state of Images

{message}

Here is the information about the Image:
    - Image Name: {name}
    - Image Extension: {extension}
    - Image Size (Bytes): {size}
    - Image URL: {url}

Regards,

Image App Team
"""


def list_sns_subscriptions():
    try:
        response = sns.list_subscriptions_by_topic(TopicArn=topic)
        subs = [
            {"email": sub["Endpoint"], "arn": sub["SubscriptionArn"]}
            for sub in response["Subscriptions"]
        ]
        return subs
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None


def subscribe_to_sns_topic(email: str):
    try:
        sns.subscribe(
            TopicArn=topic,
            Protocol="email",
            Endpoint=email,
        )
        return "Success"
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None


def delete_sns_subscription(arn: str):
    try:
        sns.unsubscribe(SubscriptionArn=arn)
        return "Success"
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None


def build_sns_message(message_from_sqs: dict):
    message_body = json.loads(message_from_sqs["Body"])
    metadata = message_body["img_metadata"]

    email = email_template.format(
        message=message_body["message"],
        name=metadata["name"],
        extension=metadata["extension"],
        size=metadata["size"],
        url=metadata["url"]
    )

    message = {
        'Id': message_from_sqs["MessageId"],
        'Message': email,
        'Subject': 'Image Update',
        'MessageAttributes': message_from_sqs["MessageAttributes"]
    }

    return message


def publish_messages_to_sns(messages: list):
    try:
        response = sns.publish_batch(
            TopicArn=topic, PublishBatchRequestEntries=messages
        )
        return response
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None