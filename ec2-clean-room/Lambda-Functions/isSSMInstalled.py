import boto3

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    response = ssm.describe_instance_information()
    print (response)
    isSSMInstalled = False

    for item in response['InstanceInformationList']:
    		if item['InstanceId'] == event['ForensicInstanceId']:
    		    isSSMInstalled = True
    		    event['SSM_STATUS'] = 'SUCCEEDED'


    event['stauscheck'] = 1
    
    return event
