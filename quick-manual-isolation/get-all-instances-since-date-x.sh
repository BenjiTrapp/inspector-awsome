#!/bin/bash

DATE_SINCE=2016-02-01
REGIONS=("us-east-1 us-west-2 us-west-1 eu-west-1 eu-central-1 ap-southeast-1 ap-northeast-1 ap-southeast-2 ap-northeast-2 sa-east-1")

function get_launched_instances_in_all_regions() {
    for region in ${REGIONS[@]};do
        echo "================================================"
        echo "Instances launched since $DATE_SINCE in $region:"
        aws ec2 describe-instances --region $region --query "Reservations[].Instances[?LaunchTime>=\`$DATE_SINCE\`][].{id: InstanceId, type: InstanceType, launched: LaunchTime}";
    done
}


# get new instance console output log
function get_instance_console_output_log() {
    if [ $# -ne 1 ]; then
        echo "ERROR - Pass instance ID as an argument"
        exit 1
    fi

    aws ec2 get-console-output --region eu-west-1 --instance-id $1
}

get_launched_instances_in_all_regions

#get_instance_console_output_log i-1234456789