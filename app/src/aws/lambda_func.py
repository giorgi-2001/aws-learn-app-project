import json
from botocore.exceptions import ClientError
from ..config import LAMBDA_ARN as lambda_arn, boto_session


lambda_client = boto_session.client("lambda")


def invoke_lambda(data: dict, arn = lambda_arn, client = lambda_client):
    try:
        payload = json.dumps(data).encode()
        response = client.invoke(
            FunctionName=lambda_arn,
            Payload=payload,
        )
        result = json.loads(response["Payload"].read())
        return result
        
    except ClientError as err:
        print("Error occured: ", err)
        return None