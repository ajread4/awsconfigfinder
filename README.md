# AWSConfigFinder

awsconfigfinder is a capability to identify anomalies in AWS Config Snapshots located in an S3 bucket. 

## Current State

Right now, the capability only finds differences in EC2 instances ([Resource Hijacking](https://attack.mitre.org/techniques/T1496/)) or the creation of new AccessKeys for a user ([Account Manipulation](https://attack.mitre.org/techniques/T1098/001/)). There are plans to build more detections in [Planned Features](#planned-features). Each of the new features plans to map to [MITRE ATT&CK](https://attack.mitre.org/matrices/enterprise/cloud/), if possible. 

# Install
```
git clone https://github.com/ajread4/awsconfigfinder.git
cd awsconfigfinder 
pip3 install -r requirements.txt
```

# Usage
```
$ python3 configfinder.py -h
usage: configfinder.py [-h] [-algo [EC2,AccessKey]] [-all] s3://snapshot1.json.gz s3://snapshot2.json.gz

awsconfigfinder - a capability to find suspicious differences between two AWS Config Snapshots.

positional arguments:
  s3://snapshot1.json.gz    first AWS Config snapshot S3 Bucket URL
  s3://snapshot2.json.gz    second AWS Config snapshot S3 Bucket URL

options:
  -h, --help            show this help message and exit
  -algo [EC2,AccessKey], --algorithm [EC2,AccessKey]    algorithm to use to analyze snapshots
  -all, --all           run all algorithms against the two snapshots
```

## Environment Variables

awsconfigfinder relies on environment variables to create a session with [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html). In order to successfuly create a session, you must add the below environment variables for the AWS IAM Role with at least read and write access to the snapshot S3 bucket and with the AWS__ConfigRole. Guidance on the AWS_ConfigRole can be found [here](https://docs.aws.amazon.com/config/latest/developerguide/security-iam-awsmanpol.html). 
```
export AWS_ACCESS_KEY_ID="<key>"
export AWS_SECRET_ACCESS_KEY="<key>"
export AWS_SECURITY_TOKEN="<token>"
export AWS_REGION="<region>"
```
If the tokens or keys are invalid or expired, awsconfigfinder will throw the following error: ```ClientError('An error occurred (InvalidToken) when calling the ListObjectsV2 operation: The provided token is malformed or otherwise invalid.')```. 

## Running Snapshots

awsconfigfinder does not run snapshots for you. Rather, it relies on two snapshots previously completed. Guidance on running snapshots within AWS can be found [here](https://docs.aws.amazon.com/config/latest/developerguide/deliver-snapshot-cli.html) with specifics about AWS Config delivery channels [here](https://docs.aws.amazon.com/config/latest/developerguide/deliver-snapshot-cli.html). 

# Examples
1. Determine if there was a new EC2 instance deployed between two snapshots to detect [Resource Hijacking](https://attack.mitre.org/techniques/T1496/). 
```
$ python3 configfinder.py s3://bucket1.json.gz s3://bucket2.json.gz -algo EC2
***EC2 Algorithm***
Difference in Number of EC2 Instances since Snaphshot 2 is larger than Snapshot 1
Unique Instance: i-06fbbf2d9707dd34b not found in first snapshot with launch time: 2023-12-03T18:41:35.000Z
```
2. Determine if new cloud credentials were created for a user to detect [Account Manipulation](https://attack.mitre.org/techniques/T1098/001/). 
```
python3 configfinder.py s3://bucket1.json.gz s3://bucket2.json.gz -algo AccessKey
***AccessKey Algorithm***
New User Access Keys Discovered for User: s20731075-d11480-sec541-sa-yft0d
New User Access Keys within Snaphshot 1
```
3. Run all algorithms against two config snapshots. 
```
python3 configfinder.py s3://bucket1.json.gz s3://bucket2.json.gz -all 
***EC2 Algorithm***
No differences detected between two provided snapshots
***AccessKey Algorithm***
New User Access Keys Discovered for User: s20731075-d11480-sec541-sa-yft0d
New User Access Keys within Snaphshot 1
```
# File and Directory Information
- ```utils``` contains the Finder class for AWS Config anomalous detection. 
- ```configfinder.py``` is the main python code that runs awsconfigfinder. 
- ```requirements.txt``` contains the necessary libraries for Python. 

# Planned Features
- Evaluate role changes between snapshots 
- Return S3 bucket changes between snapshots 
- Examine network interface changes between EC2 instances
- Discover new IAM roles
- Return new lambda functions
- And many more! 

# Author
All of the code was written by me, AJ Read. 
- [Twitter](https://twitter.com/ajread3)
- [Github](https://github.com/ajread4)
- [LinkedIn](https://www.linkedin.com/in/austin-read-88953b189/)