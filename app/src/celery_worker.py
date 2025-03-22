from celery import Celery

from .aws.sqs import (
    poll_messages_from_sqs
) 

from .aws.sns import (
    build_sns_message,
    publish_messages_to_sns
)


celery_worker = Celery(
    "celery",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery_worker.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(
        30, publish_messages, name='Publish-messages-every-30-seconds'
    )


@celery_worker.task
def publish_messages():
    print("Starting Message polling:")
    messages = poll_messages_from_sqs()
    
    if not messages:
        return print("No messages to process") 

    correctly_formated_messages = [
        build_sns_message(msg) for msg in messages
    ]

    result = publish_messages_to_sns(correctly_formated_messages)
    print(result)


celery_worker.conf.timezone = 'UTC'
celery_worker.conf.broker_connection_retry_on_startup = True