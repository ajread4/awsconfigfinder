# AWSConfigFinder

awsconfigfinder is a capability to identify anomalies in AWS Config Snapshots located in an S3 bucket. 

## Current State

Right now, the capability only finds differences in EC2 instances. There are plans to build more detections in [Planned Features](#planned-features). 

# Install
```
git clone https://github.com/ajread4/awsconfigfinder.git
cd awsconfigfinder 
pip3 install -r requirements.txt
```

# Usage
```
$ python3 configfinder.py -h
usage: configfinder.py [-h] first_snapshot second_snapshot

awsconfigfinder - a capability to find suspicious differences between two AWS Config
Snapshots.

positional arguments:
  first_snapshot   first AWS Config snapshot S3 Bucket URL
  second_snapshot  second AWS Config snapshot S3 Bucket URL

options:
  -h, --help       show this help message and exit
```

## Environment Variables

awsconfigfinder relies on environment variables to create a session with [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html). In order to successfuly create a session, you must add the below environment variables for the AWS IAM Role with at least read and write access to the snapshot S3 bucket. 
```
export AWS_ACCESS_KEY_ID="<key>"
export AWS_SECRET_ACCESS_KEY="<key>"
export AWS_SECURITY_TOKEN="<token>"
export AWS_REGION="<region>"
```
If the tokens or keys are invalid or expired, awsconfigfinder will throw the following error: ```ClientError('An error occurred (InvalidToken) when calling the ListObjectsV2 operation: The provided token is malformed or otherwise invalid.')```. 

## Examples
1. Determine if there was a new EC2 instance deployed between two snapshots. 
```
$ python3 configfinder.py s3://[S3 Bucket with First Snapshot].json.gz s3://[S3 Bucket with Second Snapshot].json.gz
Difference in Number of EC2 Instances since Snaphshot 2 is larger than Snapshot 1
Unique Instance: i-06fbbf2d9707dd34b not found in first snapshot with launch time: 2023-12-03T18:41:35.000Z
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
- Twitter[ajread3](https://twitter.com/ajread3)
- Github [ajread4](https://github.com/ajread4)
- LinkedIn [Austin Read](https://www.linkedin.com/in/austin-read-88953b189/)