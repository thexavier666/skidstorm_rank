import sys
import os
import subprocess as sp

def main():

	# directory where player data is stored
	data_dir = "data_%d"

	# name of master database
	master_db_filename = "master_db.csv"

	# getting player ID
	player_id = sys.argv[1]

	dir_list = os.listdir("./")

	# list to store current list of database directories
	data_dir_list = []

	# finding all data directories
	for i in dir_list:
		if os.path.isdir(i):
			if i[0:4] == "data":
				data_dir_list.append(i.split('_')[1])

	if len(data_dir_list) == 0:
		print "No data directory present. Bye bye"
		return 0

	# converting directory ID to integer
	data_dir_list_to_int = map(int,data_dir_list)

	# sorting them so that output is by date
	data_dir_list_to_int.sort()

	# searching player ID in all the directories
	for i in data_dir_list_to_int:
	
		cmd_str = "grep %s %s/%s | cut -d, -f 1,2,4- | column -s, -t" % (player_id, data_dir % (i), master_db_filename)

		sp.call(cmd_str,shell=True)

if __name__ == "__main__":
	main()
