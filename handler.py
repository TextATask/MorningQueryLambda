from calendar import c
import logging
import http.client
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    # Make a request to TextATask API
    conn = http.client.HTTPSConnection(f"https://${os.environ['PATH']}.execute-api.us-east-1.amazonaws.com")
    conn.request("GET", "/tasks/incomplete")
    
    response = conn.getresponse()
    
    if response.status == 200:
        print(response.json())
        data = response.read()
        logger.info("Request successful")
        return data.decode("utf-8")
    else:
        logger.error("Request failed")
        return {"statusCode": response.status, "body": response.reason}
    
    conn.close()
        