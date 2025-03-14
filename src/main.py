from fastapi import FastAPI
import requests


app  = FastAPI()


METADATA_URL = "http://169.254.169.254/latest/meta-data/"


def get_metadata(path):
    """ Helper function to fetch instance metadata """
    try:
        return requests.get(METADATA_URL + path).text
    except requests.exceptions.RequestException as err:
        print(err)
        return "Unavailable"


@app.get("/")
def get_region_and_AZ():
    availability_zone = get_metadata("placement/availability-zone")
    region = availability_zone[:-1] 

    return {
        "region": region,
        "az": availability_zone
    }
