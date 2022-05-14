import boto3
import os
ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    response = ec2.run_instances(
            ImageId=os.environ['AMI_ID'],
            InstanceType='t2.small',
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': True
            },

            IamInstanceProfile={
                'Arn': os.environ['INSTANCE_PROFILE']
            },
            # UserData = '#!/bin/bash \n cd /tmp \n sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_386/amazon-ssm-agent.rpm \n sudo amazon-ssm-agent start',

            UserData = "#!/bin/bash \n export instancehostname=$(hostname) \n sudo sed -i -e 's/127.0.0.1 localhost/127.0.0.1 localhost '$instancehostname'/g' /etc/hosts \n mkdir /tmp/ssm \n cd /tmp/ssm \n wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb \n sudo dpkg -i amazon-ssm-agent.deb \n sudo systemctl enable amazon-ssm-agent \n sudo systemctl start amazon-ssm-agent \n",
            KeyName = os.environ['EC2_KEYPAIR'],
            NetworkInterfaces = [
                {
                    'AssociatePublicIpAddress': True,
                    'DeviceIndex': 0,
                    'SubnetId': os.environ['SUBNET_ID'],
                    'Groups': [os.environ['FORENSIC_SECUTRITYGROUP']],
                }
            ],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'InstanceUnderForensics'
                        },{
                            'Key': 'IsInstanceTested',
                            'Value': 'Yes'
                        },
                    ]
                },
            ]
    )
    print (response['Instances'][0]['Placement']['AvailabilityZone'])

    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[response['Instances'][0]['InstanceId']])
    event['ForensicInstanceId'] = response['Instances'][0]['InstanceId']
    event['availabilityZone'] = response['Instances'][0]['Placement']['AvailabilityZone']
    event['SSM_STATUS'] ='WAIT'
    return event
