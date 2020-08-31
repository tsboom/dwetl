import os
import shutil
import time
import sys
# main function
def main():
	arguments = sys.argv
	if '--help' in arguments:
		print('Usage: ')
        	print('\tezproxy_etl.py path data_type')
        	print('\t example usage: python delete_processed_files.py /apps/dw/processed/ezproxy/ aleph')
        	sys.exit(1)

	if len(arguments) < 4:
        	print('Usage: ')
        	print('\tezproxy_etl.py path data_type')
        	print('\t example usage: python delete_processed_files.py /apps/dw/processed/ezproxy/ aleph')
        	sys.exit(1)

	if len(arguments) == 4:
		path = arguments[1]
		#folder delete (aleph) or file delete (ezproxy)
		delete_type = arguments[2]
		#retention policy
		days = arguments[3]
		days =float(days)
	seconds = time.time() - (days * 24 * 60 * 60)
	# checking whether the file is present in path or not
	if os.path.exists(path):
		if delete_type == "aleph":
		# iterating over each and every folder and file in the path
			for root_folder, folders, files in os.walk(path):
				# removing the folders within the directory
				for folder in folders:
					# folder path
					folder_path = os.path.join(root_folder, folder)
					if seconds >= get_file_or_folder_age(folder_path):
						remove_folder(folder_path)
					else:
						print("no processed aleph files older than the assigned retention policy")
		else:
			for root_folder, folders, files in os.walk(path):
				for file in files:
					# file path
					file_path = os.path.join(root_folder, file)
					if seconds >= get_file_or_folder_age(file_path):
						# removing the files within the directory
						remove_file(file_path)
					else:
						 print("no processed  ezproxy files older than the assigned retention policy")

	else:

		# file/folder is not found
		print('path is not found')


def remove_folder(path):
	# removing the folder
	if not shutil.rmtree(path):
		# success message
		print("%s was removed successfully." % path)
	else:
		# failure message
		print("Unable to delete %s" % path)



def remove_file(path):
	# removing the file
	if not os.remove(path):
		# success message
		print("%s was removed successfully." % path)
	else:
		# failure message
		print("Unable to delete %s" % path)

def get_file_or_folder_age(path):
	# getting ctime of the file/folder in seconds
	ctime = os.stat(path).st_ctime
	return ctime

if __name__ == '__main__':
	main()

