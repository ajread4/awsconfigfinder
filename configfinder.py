import argparse
from utils.finder import Finder

def main():
	"""
	Main function for awsconfigfinder
	"""
	parser = argparse.ArgumentParser(description='awsconfigfinder - a capability to find suspicious differences between two AWS Config Snapshots.')
	parser.add_argument('first_snapshot', action='store', help='first AWS Config snapshot S3 Bucket URL',metavar='first_snapshot')
	parser.add_argument('second_snapshot', action='store', help='second AWS Config snapshot S3 Bucket URL',metavar='second_snapshot')

	# Parse the arguments
	args=parser.parse_args()

	# Instantiate the Finder Class
	configfinder=Finder()

	# Find Anomalous EC2 Instances
	configfinder.find_EC2(args.first_snapshot,args.second_snapshot)

if __name__=="__main__":
	try:
		main()
	except Exception as err:
		print(repr(err))