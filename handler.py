import logging
import http.client
import os
import base64
import json
import urllib
from urllib import request, parse

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/"
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TO_NUMBER = os.environ['TO_NUMBER']
FROM_NUMBER = os.environ['FROM_NUMBER']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    # Make a request to TextATask API
    conn = http.client.HTTPSConnection(f"{os.environ['PATH']}.execute-api.us-east-1.amazonaws.com")
    conn.request("GET", "/tasks/incomplete")
    
    response = conn.getresponse()
    
    if response.status == 200:
        data = response.read()
        logger.info("Request successful")
        body = data.decode("utf-8")
        tasks = []
        for task in body:
            task_details = json.loads(task)
            tasks.append(task_details["id"], task_details["text"])
            #
        message = f"Good Morning, These are your incomplete tasks for today: \n{tasks}"
    else:
        logger.error("Request failed")
        return {"statusCode": response.status, "body": response.reason}
    

    if not TWILIO_ACCOUNT_SID:
        return "Unable to access Twilio Account SID."
    elif not TWILIO_AUTH_TOKEN:
        return "Unable to access Twilio Auth Token."
    elif not TO_NUMBER:
        return "The function needs a 'To' number in the format +12023351493"
    elif not FROM_NUMBER:
        return "The function needs a 'From' number in the format +19732644156"
    elif not body:
        return "The function needs a 'Body' message to send."

    # insert Twilio Account SID into the REST API URL
    url = f"{TWILIO_SMS_URL}{TWILIO_ACCOUNT_SID}/Messages.json"
    post_params = {"To": TO_NUMBER, "From": FROM_NUMBER, "Body": message}

    #encode the parameters for a Python's urllib request
    full_data = parse.urlencode(post_params).encode("utf-8")
    req = request.Request(url)

    # provide the credentials for Twilio
    authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    base64string = base64.b64encode(authentication.encode("utf-8"))
    req.add_header("Authorization", "Basic %s" % base64string.decode("ascii"))


    try:
        #perform request to Twilio API
        with request.urlopen(req, full_data) as f:
            logger.info("Twilio API request successful")
            print(f.read().decode("utf-8"))
    except Exception as e:
        logger.error("Twilio API request failed")
        return e
    
    
    conn.close()

    return {"statusCode": 200, "body": "Message sent successfully!"}
    
        