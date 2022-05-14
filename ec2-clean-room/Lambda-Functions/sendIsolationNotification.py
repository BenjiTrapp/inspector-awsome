import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

s3 = boto3.client('s3')

HOOK_URL = os.environ['HookUrl']
SLACK_CHANNEL = os.environ['SlackChannel']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    instanceID = event['instanceID']
    targetGroupArn = event['targetGroupArn']
    slack_message_text = formatMyMessage(instanceID, targetGroupArn)
    req = Request(HOOK_URL, json.dumps(slack_message_text).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", SLACK_CHANNEL)
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
 
    return event

def formatMyMessage(instanceID, targetGroupArn):
    slack_message = {
        "attachments": [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "color": "#b7121a",
                "title": "High Alert!! \n Security Incident detected \n Instance Isolated due to security incident detected by guard duty from ALB : " +  instanceID ,
                "text": "",
                "fields":[{
                        "value": "Next Steps : " + '\n 1. Snapshot of the volume will be created \n 2. Snapshot will be mounted into volume for Forsensic Analysis \n 3. New Forensic Instance will be created and the volume will be mounted for forensic analysis \n 4. Forensic report will sent to security channel'
                    },
                    {
                        "value": "Instance under isolation: " + instanceID
                    },
                    {
                        "value": "TargetGroup ARN where instance is drained from : " + targetGroupArn
                    }]
            }
        ]
    }
    return slack_message