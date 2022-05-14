import boto3
import os

def lambda_handler(event, context):
    print (event)
    client = boto3.client('ec2')
    instanceID = event.get('instanceID')
    response = client.describe_instances(

        InstanceIds=[
            instanceID
        ]
    )
    volumeID = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    print (volumeID)
    SnapShotDetails = client.create_snapshot(
        Description='Isolated Instance',
        VolumeId=volumeID
    )
    print (response)
    print (SnapShotDetails['SnapshotId'])

    response = client.modify_instance_attribute(

        Groups=[
            os.environ['ISOLATED_SECUTRITYGROUP'],
        ],
        InstanceId=instanceID
    )

    tagresponse = client.create_tags(

        Resources=[
            instanceID,
        ],
        Tags=[
            {
                'Key': 'IsIsolated',
                'Value': 'InstanceIsolated'
            },
        ]
    )

    waiter = client.get_waiter('snapshot_completed')
    waiter.wait(
        SnapshotIds=[
            SnapShotDetails['SnapshotId'],
        ]
    )
    return SnapShotDetails['SnapshotId']
