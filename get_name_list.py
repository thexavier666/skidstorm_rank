import json
import urllib
import unicodecsv as csv	# you need to install this
import sys
import os

def const_RANK_JSON(rank_range):
	return "all_rank_%s.json" % (rank_range)

def const_USER_JSON(device_id):
	return "user_%s.json" % (device_id)

def const_CSV_FILE_NAME(rank_range):
	return "user_id_%s.csv" % (rank_range)

# fetches all data from main rank
def fetch_data_all(rank_range):
	ss_ip = "150.109.0.114"
	ss_url = "http://%s/v/rank/list/%s/ALL"

	full_url = ss_url % (ss_ip, rank_range)

	urllib.urlretrieve(full_url, const_RANK_JSON(rank_range))

# fetches data for a particular player
# from the complete data, returns only the user ID
def fetch_data_userid(device_id):
	ss_ip = "150.109.0.114"
	ss_user_url = "http://%s/v/profile/%s"

	full_user_url = ss_user_url % (ss_ip, device_id)

	urllib.urlretrieve(full_user_url, const_USER_JSON(device_id))

# gets the user ID for the current user
def get_userid(device_id):
	json_user_file_name = const_USER_JSON(device_id)

	json_dic = json.load(open(json_user_file_name, 'r'))

	user_id = json_dic["profile"]["id"]

	return user_id

# gets all ranks with userID and device ID
def get_ranks(rank_range):
	json_file_name = const_RANK_JSON(rank_range)

	json_dic = json.load(open(json_file_name,'r'))

	l_name_dev = []

	lim = 100
	lim_cnt = 0

	for i in json_dic["ranks"]:
		# getting username and device ID of current user
		tmp_data_extract = [i["username"], i["device"]]

		# fetching the complete data of the current user
		fetch_data_userid(i["device"])

		# from the complete data of the user, getting only the user ID
		curr_player_userid = get_userid(i["device"])

		tmp_data_extract.insert(0,curr_player_userid)

		l_name_dev.append(tmp_data_extract)

		print tmp_data_extract

		# deleting the user data json file once the work is done
		os.remove(const_USER_JSON(i["device"]))

		if lim_cnt < lim:
			lim_cnt += 1
		else:
			break

		print "rank " + str(lim_cnt) + " done"

	for i in l_name_dev:
		print i

	# writing the list in a csv file
	fp = open(const_CSV_FILE_NAME(rank_range), 'wb')
	wr = csv.writer(fp)
	wr.writerows(l_name_dev)

def main():	
	ss_rank_range = ["1-100", "100-200", "201-300", "301-400", "401-500"]

	# this should range from 0-4 inclusive
	rank_choice = int(sys.argv[1])

	# fetches complete rank data
	# disable this line if you have already fetched the complete rank data once
	fetch_data_all(ss_rank_range[rank_choice])

	# extracting data from json
	get_ranks(ss_rank_range[rank_choice])

if __name__ == "__main__":
	main()
