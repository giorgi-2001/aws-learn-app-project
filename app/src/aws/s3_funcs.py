import os

from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

from ..config import S3_BUCKET, boto_session


load_dotenv()


bucket_name = S3_BUCKET


def get_image_metadata(image_name: str):
    s3 = boto_session.client('s3')

    image_path = f"images/{image_name}"

    try:
        response = s3.head_object(Bucket=bucket_name, Key=image_path)
        metadata = {
            "name": image_name,
            "last_update": response['LastModified'],
            "size": response['ContentLength'],
            "extension": os.path.splitext(image_name)[1]
        }
        print("Response", response)
        return metadata
    
    except NoCredentialsError:
        print("Credentials not available")
        return None
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(f"The object {image_name} does not exist in the bucket {bucket_name}.")
        else:
            print(f"An error occurred: {e}")
        return None
    

def generate_presigned_url(name: str, expiration: int = 3600):
    s3 = boto_session.client('s3')

    image_path = f"images/{name}"

    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": image_path},
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None