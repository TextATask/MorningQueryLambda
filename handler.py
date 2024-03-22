import logging
import requests
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    # Make a request to TextATask API    
    url = f"https://${os.environ['PATH']}.execute-api.us-east-1.amazonaws.com/tasks/incomplete"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        logger.info("Request was successful")
        return response.json()
    else:
        logger.error("Request failed")
        return {"statusCode": response.status_code, "body": response.text}
        