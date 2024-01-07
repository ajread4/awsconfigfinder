import argparse
from utils.finder import Finder

def main():
	"""
	Main function for awsconfigfinder
	"""
	parser = argparse.ArgumentParser(description='awsconfigfinder - a capability to find suspicious differences between two AWS Config Snapshots.')
	parser.add_argument('first_snapshot', action='store', help='first AWS Config snapshot S3 Bucket URL',metavar='s3://snapshot1.json.gz')
	parser.add_argument('second_snapshot', action='store', help='second AWS Config snapshot S3 Bucket URL',metavar='s3://snapshot2.json.gz')
	parser.add_argument('-algo','--algorithm',action='store',help='algorithm to use to analyze snapshots',metavar='[EC2,AccessKey]')
	parser.add_argument('-all','--all',action="store_true", help="run all algorithms against the two snapshots")

	# Parse the arguments
	args=parser.parse_args()

	# Instantiate the Finder Class
	configfinder=Finder()

	if not args.all: 
		if (args.algorithm == 'EC2'):
			print('***EC2 Algorithm***')
			configfinder.find_EC2(args.first_snapshot,args.second_snapshot)
		elif (args.algorithm == 'AccessKey'):
			print('***AccessKey Algorithm***')
			configfinder.find_AccessKey(args.first_snapshot,args.second_snapshot)
		else: 
			print("***Incorrect Algorithm***")
	else: 
		print('***EC2 Algorithm***')
		configfinder.find_EC2(args.first_snapshot,args.second_snapshot)
		print('***AccessKey Algorithm***')
		configfinder.find_AccessKey(args.first_snapshot,args.second_snapshot)

if __name__=="__main__":
	try:
		main()
	except Exception as err:
		print(repr(err))