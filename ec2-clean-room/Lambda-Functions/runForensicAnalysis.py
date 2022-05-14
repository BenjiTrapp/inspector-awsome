import boto3
import os

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    
    
    instanceID = event['instanceID']
    S3BucketName = os.environ['OUTPUT_S3_BUCKETNAME']
    S3BucketRegion = os.environ['OUTPUT_S3_BUCKETREGION']
    commands = ['#!/bin/bash','printf -v date "%(%F)T" -1', 'sudo mkdir /forensics','dd if=/dev/xvdb1 of=/forensics/i-23sdf5esdf.dd' ,'fls -r -m -i /forensics/i-23sdf5esdf.dd >/home/ubuntu/file-full-i-23sdf5esdf.txt', 'mactime -b /home/ubuntu/file-full-i-23sdf5esdf.txt $date >/home/ubuntu/file-2018-i-23sdf5esdf.txt', 'fls -rd /forensics/i-23sdf5esdf.dd >/home/ubuntu/file-deleted-i-23sdf5esdf.txt', 'sudo apt-get install cloud-utils ','EC2_INSTANCE_ID=$(ec2metadata --instance-id)', 'cp /home/ubuntu/file-deleted-i-23sdf5esdf.txt /home/ubuntu/file-deleted-$EC2_INSTANCE_ID-' + instanceID+ '.txt', 'cp /home/ubuntu/file-2018-i-23sdf5esdf.txt /home/ubuntu/$EC2_INSTANCE_ID.txt', 'cp /home/ubuntu/file-full-i-23sdf5esdf.txt /home/ubuntu/file-full-$EC2_INSTANCE_ID.txt', 'aws s3 cp /home/ubuntu/file-full-$EC2_INSTANCE_ID.txt s3://' + S3BucketName+ '/incident-response/file-full-$EC2_INSTANCE_ID.txt','aws s3 cp /home/ubuntu/file-deleted-$EC2_INSTANCE_ID-' + instanceID+ '.txt s3://' + S3BucketName + '/incident-response/file-deleted-$EC2_INSTANCE_ID-' + instanceID+ '.txt', 'aws s3 cp /home/ubuntu/$EC2_INSTANCE_ID.txt s3://' + S3BucketName +'/incident-response/$EC2_INSTANCE_ID.txt']
    
    
    response = ssm.send_command(
            InstanceIds= [event.get('ForensicInstanceId')],
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': commands,
                'executionTimeout': ['600']
            },
            Comment='SSM Command Execution',
            OutputS3Region=S3BucketRegion,
            OutputS3BucketName=S3BucketName,
            OutputS3KeyPrefix=event.get('ForensicInstanceId')

        )
    print (response)
    return event
