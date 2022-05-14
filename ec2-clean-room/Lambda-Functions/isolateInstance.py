import boto3
elb = boto3.client('elbv2')

def isolateInstance (instanceID, targetGroupsARN) :
    print(instanceID)
    print(targetGroupsARN)
    response = elb.deregister_targets(
        TargetGroupArn=targetGroupsARN,
        Targets=[
                {
                    'Id': instanceID
                },
            ]
    )
    print (response)
    return 'SUCCEEDED'


def lambda_handler(event, context):

    instanceID = event.get('instanceID')
    response = 'FAILED'
    targetGroups = elb.describe_target_groups()
    
    for key in targetGroups['TargetGroups']:
        targetGroupArn = key.get('TargetGroupArn')
        targets = elb.describe_target_health(
            TargetGroupArn=targetGroupArn
        )

        instanceIDlist = []
        for instanceKey in targets['TargetHealthDescriptions']:
            instanceIDlist.append(instanceKey.get('Target').get('Id'))

        if instanceID in instanceIDlist:
            response = isolateInstance(instanceID, targetGroupArn)
    event['STATUS'] = response
    event['targetGroupArn'] = targetGroupArn
    return event
