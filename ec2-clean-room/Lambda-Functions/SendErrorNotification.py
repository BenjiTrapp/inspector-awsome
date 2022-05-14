import boto3
import json
import logging
import os
import requests

s3 = boto3.client('s3')

HOOK_URL = os.environ['HookUrl']
SLACK_CHANNEL = os.environ['SlackChannel']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    download_path = '/tmp/key.txt'
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )
    content = response['Body'].read()
    array = []
    linearray = content.splitlines()
    
    for s in linearray:
        if "d/r *" in str(s):
            array.append('"' + str(s) + '"')

    print (array)
    instanceList = key.replace('incident-response/file-deleted-', '').replace(".txt", "");
    print (instanceList)
    instanceArray = instanceList.split("-i-")
    slack_message_text = formatMyMessage("i-" + instanceArray[1],instanceArray[0], array, "s3://" + bucket + "/" + key)
    response = requests.post(HOOK_URL, data=json.dumps(slack_message_text), headers={'Content-Type': 'application/json'})
    logging.info("Response Status Code: ")
    return slack_message_text

def formatMyMessage(victimInstanceID, instanceID, deletedLines, s3location):

    slack_message = {
        "attachments": [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "color": "#b7121a",
                "title": "Results for instance " +  victimInstanceID + " being investigated for deleted files\n " +" \n For more information login to forensics instance : " +  instanceID + " \n AWS Account: " + "469306637372" + " \n S3 Location: " + s3location ,
                "text": "",
                "fields":[{
                        "value": "Details: " + '\n '.join(deletedLines)
                    },
                    {
                        "value": "For More details Login to the instance: " + instanceID
                    }]
            }
        ]
    }
    return slack_message
