<br/>
<div id="logo" align="center">
    <br />
    <img src="docs/inspector.png" alt="Logo" width="222"/>
    <h3>Inspector Awesome</h3>
</div>
<br>

Tiny collection of scripts to isolate an EC2 instance and start with the joy of forensics.

In the case of a compromised EC2 instance within your fleet, it's time for getting prepared for Incident Response and Threat Hunting. To get started you have two Options:

1. Use the manual bash scripts located in `quick-manual-isolation` 
2. A predefined Step-Function that helps you to automate the isolation step as much as possible

## Quick Manual Isolation with some Bash Kung-Fu

You'll find the following scripts:

| Script name                       | Semantics                                                                |
| ----------------------------------|--------------------------------------------------------------------------|
| get-all-instances-since-date-x.sh | Collect all instances based on a given date as a starting date           |
| isolate-ec2-instance-internal.sh  | Isolate the EC2 instance from within the instance (use SSM for that)     |
| isolate-ec2-instance-external.sh  | Isolate the EC2 instance from your local machine and the help of AWS CLI |

## Step Function Kung-Fu

The easiest way in is this overview:


<p align="center">
<img width="600" src="docs/clean-room-stepfunction.png">
</p>

Like shown above - the StepFunction will take an instance ID passed by an SNS topic through a series of Lambda Functions. During the execution the Step Function will automatically notify, isolate and run basic forensics.

## Disclaimer 

I'm not responsible for any misuse, mistakes and possible loss of money by executing those scripts
