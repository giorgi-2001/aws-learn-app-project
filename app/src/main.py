from fastapi import FastAPI
import requests


app  = FastAPI()


def get_ec2_metadata_token():
    """
    Get the EC2 metadata session token (IMDSv2).
    """
    metadata_url = "http://169.254.169.254/latest/api/token"
    headers = {
        "X-aws-ec2-metadata-token-ttl-seconds": "21600"
    }
    
    try:
        response = requests.put(metadata_url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error getting metadata token: {e}")
        return None


def get_az_info(token):
    """
    Get EC2 Availability Zone information using the session token.
    """
    metadata_url = "http://169.254.169.254/latest/meta-data/placement/availability-zone"
    headers = {
        "X-aws-ec2-metadata-token": token
    }
    
    try:
        response = requests.get(metadata_url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error getting AZ info: {e}")
        return None



@app.get("/")
def get_region_and_AZ():
    token = get_ec2_metadata_token()
    availability_zone = get_az_info(token)
    region = availability_zone[:-1] 

    return {
        "region": region,
        "az": availability_zone
    }
