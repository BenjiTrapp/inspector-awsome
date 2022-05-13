#!/bin/bash

# My system IP/set ip address of server
MY_OWN_IP="YOUR.PUBLIC.IP.ADDR"
SG_BLOCK_ID="sg-BLOCK-ID"
VPC_ID="vpc-1a2b3c4d"
CLASSIC_EC2_INSTANCE=false

function create_sec_group_for_isolate_classic_instance() {
    aws ec2 create-security-group --group-name isolation-sg --description "Security group for isolating EC2-Classic instances"
}

function create_sec_group_for_isolation() {
    aws ec2 create-security-group --group-name isolation-sg --description "Security group to isolate a EC2-VPC instance" --vpc-id ${VPC_ID}
}

function allow_ssh_access_only_from_own_public_ip() {
    dig +short myip.opendns.com @resolver1.opendns.com
    aws ec2 authorize-security-group-ingress --group-name isolation-sg --protocol tcp --port 22 --cidr ${MY_OWN_IP}/32
    aws ec2 authorize-security-group-ingress --group-id ${SG_BLOCK_ID} --protocol tcp --port 22 --cidr ${MY_OWN_IP}/32 
    # note the difference between both commands in group-name and group-id, sg-BLOCK-ID is the ID of your isolation-sg
}

function totally_block_outbund_traffic() {
    aws ec2 revoke-security-group-egress --group-id ${SG_BLOCK_ID} --protocol '-1' --port all --cidr '0.0.0.0/0' 
}

function remove_rule_that_allows_all_outbound_traffic() {
    aws ec2 authorize-security-group-egress --group-id ${SG_BLOCK_ID} --protocol 'tcp' --port 80 --cidr '0.0.0.0/0' 
    # place a port or IP if you want to enable some other outbound traffic otherwise do not execute this command.
}

function isolate_compromised_instance() {
    if [ $CLASSIC_EC2_INSTANCE = true ]; then
        create_sec_group_for_isolate_classic_instance
    else
        create_sec_group_for_isolation
    fi

    allow_ssh_access_only_from_own_public_ip
    totally_block_outbund_traffic
    remove_rule_that_allows_all_outbound_traffic
}

#Apply that Security Group to the compromised instance:
function apply_sg_to_compromized_instance() {
    aws ec2 modify-instance-attribute --instance-id i-INSTANCE-ID --groups ${SG_BLOCK_ID} 
    # where sg-BLOCK-ID is the ID of your isolation-sg

}

isolate_compromised_instance
apply_sg_to_compromized_instance
