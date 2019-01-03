import json
import urllib
import sys
import os			# for deleting user json files
import unicodecsv as csv	# for writing spl. characters into file in UNICODE

########## SOME CONSTANTS ###########

# returns file name of a certain rank range
def const_RANK_JSON(rank_range):
	return "all_rank_%s.json" % (rank_range)

# returns file name of a user based on device ID
def const_USER_JSON(device_id):
	return "user_%s.json" % (device_id)

# returns file name of user details of a certain rank range
def const_CSV_FILE_NAME(rank_range):
	return "user_id_%s.csv" % (rank_range)

def const_SS_IP():
	return "api.skidstorm.cmcm.com"

#####################################

# fetches all data from main rank
def fetch_data_all(rank_range):
	ss_ip = const_SS_IP()
	ss_url = "http://%s/v/rank/list/%s/ALL"

	full_url = ss_url % (ss_ip, rank_range)

	while True:

		urllib.urlretrieve(full_url, const_RANK_JSON(rank_range))

		if os.path.isfile(const_RANK_JSON(rank_range)) == True:
			break

	# file has been fetched

# fetches data for a particular player from the Skidstorm server
# from the complete data, returns only the user ID
def fetch_data_userid(device_id):
	ss_ip = const_SS_IP()
	ss_user_url = "http://%s/v/profile/%s"

	full_user_url = ss_user_url % (ss_ip, device_id)

	while True:

		urllib.urlretrieve(full_user_url, const_USER_JSON(device_id))

		if os.path.isfile(const_USER_JSON(device_id)) == True:
			break

	# file has been fetched

# gets the user ID for the current user from the json file
def get_userid(device_id):
	json_user_file_name = const_USER_JSON(device_id)

	json_dic = json.load(open(json_user_file_name, 'r'))

	user_id = json_dic["profile"]["id"]

	return user_id

def get_legendary_trophy(device_id):
	json_user_file_name = const_USER_JSON(device_id)

	json_dic = json.load(open(json_user_file_name, 'r'))

	user_leg_trophy = json_dic["profile"]["legendaryTrophies"]

	return user_leg_trophy

# returns integer version of the string ranks
def get_rank_range_integer(rank_range):
	return map(int,rank_range.split("-"))

# calculates rank range from rank page numberi
# if input is 1, output="1-100"
# if input is 2, output="101-200" and so on
def get_rank_range_from_rank_choice(rank_choice):
	
	# calculating rank limits
	upper_lim = rank_choice * 100
	lower_lim = upper_lim - 99

	rank_range = "%d-%d" % (lower_lim,upper_lim)

	return rank_range

def get_user_all_data(i):

	# getting device id of the current user
	user_dev_id = i["device"]

	# fetching the complete data of the current user
	fetch_data_userid(user_dev_id)

	# from the complete data of the user, getting the user ID and legendary trophy
	user_game_id 	= get_userid(user_dev_id)
	user_leg_trophy = get_legendary_trophy(user_dev_id)

	user_name 	= i["username"]
	clan_id 	= i["clanId"]
	clan_tag 	= i["clanTag"]
	user_country 	= i["country"]
	user_trophy	= i["rank"]

	# checking if the user belongs to a clan
	if clan_id == None:
		clan_id = 0
		clan_tag= "<NO_CLAN>"

	# creating the tuple for the current user
	# more can be added but please append to this list
	# to maintain compatibility

	tmp_data_extract = [user_game_id,user_name,user_dev_id,user_country,clan_tag,clan_id,user_trophy,user_leg_trophy]

	return tmp_data_extract
	
# gets all ranks with userID and device ID
def get_ranks(rank_range):
	json_file_name = const_RANK_JSON(rank_range)

	json_dic = json.load(open(json_file_name,'r'))

	# list to store all the data
	l_name_dev = []

	# getting lower limit of the rank range in integer
	lim_cnt = get_rank_range_integer(rank_range)[0]

	for each_player in json_dic["ranks"]:

		# gathering a tuple of data for user 'i'
		tmp_data_extract = get_user_all_data(each_player)

		# adding the tuple to the main list
		l_name_dev.append(tmp_data_extract)

		# deleting the user data json file once the work is done
		os.remove(const_USER_JSON(i["device"]))

		print "Rank %s %s" % (str(lim_cnt), tmp_data_extract)

		lim_cnt += 1

	# writing the list in a csv file
	fp = open(const_CSV_FILE_NAME(rank_range), 'wb')
	wr = csv.writer(fp)
	wr.writerows(l_name_dev)

def main():	

	# input = 1 means rank 1-100
	# input = 2 means rank 101-200 and so on
	rank_choice = int(sys.argv[1])

	# getting rank range based on input from user
	rank_range = get_rank_range_from_rank_choice(rank_choice)

	# fetches complete rank data from Skidstorm Servers
	fetch_data_all(rank_range)

	# extracting data from json
	get_ranks(rank_range)

if __name__ == "__main__":
	main()
