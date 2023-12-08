import awswrangler as wr
import pandas as pd
import boto3
import botocore
import json
import os 

class Finder():

	def __init__(self):

		# Instantiate Keys and Tokens
		self.aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
		self.aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
		self.aws_session_token=os.getenv('AWS_SECURITY_TOKEN')
		self.region=os.getenv('AWS_REGION')

		# Create Session 
		self.my_session=boto3.Session(aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, aws_session_token=self.aws_session_token, region_name=self.region)

	# Reformat the Pandas Dataframe for Configuration Items
	def find_configurationItems(self,snapshot):
		initial_df=wr.s3.read_json(path=snapshot,boto3_session=self.my_session)
		new_df=[]
		for i in range(len(initial_df)):
			row=initial_df.iloc[i]
			new_df.append(row.configurationItems)
		return pd.DataFrame(new_df)


	# Reformat the Pandas DataFrame for the configuration section 
	def find_configuration(self,df):
		new_df=[]
		for i in range(len(df)):
			row=df.iloc[i]
			new_df.append(row.configuration)
		return pd.DataFrame(new_df)

	# Drill down on only EC2 Instances within the Snapshot
	def parse_EC2Instance(self, df):
		return df[df['resourceType']=='AWS::EC2::Instance']

	# Find difference in instances between two Snapshots
	def find_EC2(self, first_snapshot,second_snapshot):
		snapshot1_df=self.find_configurationItems(first_snapshot)
		snapshot2_df=self.find_configurationItems(second_snapshot)

		snapshot1_df=self.parse_EC2Instance(snapshot1_df)
		snapshot2_df=self.parse_EC2Instance(snapshot2_df)

		snapshot1_df=self.find_configuration(snapshot1_df)
		snapshot2_df=self.find_configuration(snapshot2_df)

		# Set a difference variable 
		EC2_diff=False

		# If the first snaphshot has more instances than the second 
		if len(snapshot1_df) > len(snapshot2_df):
			print("Difference in Number of EC2 Instances since Snaphshot 1 is larger than Snapshot 2") 
			for row in snapshot1_df.itertuples(): 
				df1=snapshot1_df[snapshot1_df['instanceId']==str(row.instanceId)]
				df2=snapshot2_df[snapshot2_df['instanceId']==str(row.instanceId)]
				if df1.empty:
					print(f"Unique Instance: {row.instanceId} not found in first snapshot with launch time: {row.launchTime}")
					EC2_diff=True 
				if df2.empty: 
					print(f"Unique Instance: {row.instanceId} not found in second snapshot with launch time: {row.launchTime}")
					EC2_diff=True 					
			if not EC2_diff: 
				print(f"No differences detected between two provided snapshots")

		# If the second snapshot has more instances than the first 
		elif len(snapshot2_df) > len(snapshot1_df):
			print("Difference in Number of EC2 Instances since Snaphshot 2 is larger than Snapshot 1") 
			for row in snapshot2_df.itertuples(): 
				df1=snapshot1_df[snapshot1_df['instanceId']==str(row.instanceId)]
				df2=snapshot2_df[snapshot2_df['instanceId']==str(row.instanceId)]
				if df1.empty:
					print(f"Unique Instance: {row.instanceId} not found in first snapshot with launch time: {row.launchTime}")
					EC2_diff=True 
				if df2.empty:
					print(f"Unique Instance: {row.instanceId} not found in second snapshot with launch time: {row.launchTime}")
					EC2_diff=True 
			if not EC2_diff: 
				print(f"No differences detected between two provided snapshots")

		# If the snapshots have the same number of instances 
		else: 
		    for row in snapshot1_df.itertuples(): 
		        df1=snapshot1_df[snapshot1_df['instanceId']==str(row.instanceId)]
		        df2=snapshot2_df[snapshot2_df['instanceId']==str(row.instanceId)]
		        if df1.empty:
		        	print(f"Unique Instance: {row.instanceId} not found in first snapshot with launch time: {row.launchTime}")
		        	EC2_diff=True 
		        if df2.empty:
		        	print(f"Unique Instance: {row.instanceId} not found in second snapshot with launch time: {row.launchTime}")
		        	EC2_diff=True 
		    if not EC2_diff: 
		        print(f"No differences detected between two provided snapshots")
