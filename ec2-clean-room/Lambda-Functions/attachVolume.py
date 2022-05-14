import boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    volumeresponse = ec2.create_volume(
        AvailabilityZone=event.get('availabilityZone'),
        Size=100,
        SnapshotId=event.get('snapshotID'),
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Isolated VOLUME'
                    },
                ]
            },
        ]
    )
    waiter = ec2.get_waiter('volume_available')

    waiter.wait(
        VolumeIds=[volumeresponse['VolumeId']]
    )
    response = ec2.attach_volume(
        InstanceId=event.get('ForensicInstanceId'),
        VolumeId=volumeresponse['VolumeId'],
        Device='/dev/sda2',

    )
    event['wait_time'] = 60
    return event
