import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Have to echo this during the user data execution
S3_BUCKET = os.environ.get("S3_BUCKET")
DB_URL = os.environ.get("DB_URL")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


boto_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
