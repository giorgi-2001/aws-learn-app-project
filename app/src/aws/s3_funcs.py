import os
import io

from botocore.exceptions import NoCredentialsError, ClientError

from ..config import S3_BUCKET, boto_session


bucket_name = S3_BUCKET


def get_image_metadata(image_name: str):
    s3 = boto_session.client('s3')

    image_path = f"images/{image_name}"

    try:
        response = s3.head_object(Bucket=bucket_name, Key=image_path)
        metadata = {
            "name": image_name,
            "size": response['ContentLength'],
            "extension": os.path.splitext(image_name)[1]
        }
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

    params = {
        'Bucket': bucket_name,
        'Key': image_path,
        'ResponseContentDisposition': f'attachment; filename="{name}"'
    }

    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None
    

def upload_image_to_s3(name: str, content: bytes):
    s3 = boto_session.client('s3')

    file_path = f"images/{name}"
    file_stream = io.BytesIO(content)
    
    try:
        s3.upload_fileobj(file_stream, bucket_name, file_path)
        print(f"Image uploaded successfully to s3://{bucket_name}/{file_path}")
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except NoCredentialsError:
        print("Error: No valid AWS credentials found.")
    except Exception as e:
        print(f"Error uploading image: {e}")


def delete_image_from_s3(name: str):
    s3 = boto_session.client('s3')

    file_path = f"images/{name}"
    
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_path)
        print(f"Image removed successfully from s3://{bucket_name}/{file_path}")
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except NoCredentialsError:
        print("Error: No valid AWS credentials found.")
    except Exception as e:
        print(f"Error uploading image: {e}")
