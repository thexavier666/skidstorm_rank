#!/usr/bin/python3

import json
import requests
import sys
import os			# for deleting user json files
import unicodecsv as csv	# for writing spl. characters into file in UNICODE

########## ARGUMENTS ###########

# argument 1 = numeric | which rank page to fetch
# argument 2 = numeric | in which folder to keep the collected data
# argument 3 = binary  | 0 : default fetch, 1 : don't fetch user ID, fetches are much faster

########## CONSTANTS ###########

def const_NUM_DATA_POINT():
	return 200

def const_DATA_DIR(num = sys.argv[2]):
	return "data_%s/" % (num)

# returns file name of a certain rank range
def const_RANK_JSON(rank_range):
	return "%sall_rank_%s.json" % (const_DATA_DIR(), rank_range)

# returns file name of a user based on device ID
def const_USER_JSON(device_id):
	return "%suser_%s.json" % (const_DATA_DIR(), device_id)

# returns file name of user details of a certain rank range
def const_CSV_FILE_NAME(rank_range):
	return "%suser_id_%s.csv" % (const_DATA_DIR(), rank_range)

def const_SS_IP():
	return "api.skidstorm.cmcm.com"

def const_SS_URL_FORMAT():
	return "http://%s/v2/rank/list/%s/ALL"

def const_SS_USER_URL_FORMAT():
	return "http://%s/v2/profile/%s"

def const_ERROR_FILE():
	return "error_file_%s" % (sys.argv[2])

#####################################

# fetches all data from main rank
def fetch_data_all(rank_range):
	ss_ip = const_SS_IP()
	ss_url = const_SS_URL_FORMAT()

	full_url = ss_url % (ss_ip, rank_range)

	while True:
		response_obj = requests.get(full_url)

		if response_obj.status_code == 200:
			json.dump(response_obj.json(),open(const_RANK_JSON(rank_range),"w"))
			print("[RANK SUCCESS] Fetch for range %s finished" % (rank_range))

			return
		else:
			print("[RANK ERROR] D/L FAILED FOR %s. TRYING AGAIN!" % (rank_range))

# fetches data for a particular player from the Skidstorm server
# from the complete data, returns only the user ID
def fetch_data_userid(device_id):
	ss_ip = const_SS_IP()
	ss_user_url = const_SS_USER_URL_FORMAT()

	full_user_url = ss_user_url % (ss_ip, device_id)

	try:
		while True:

			response_obj = requests.get(full_user_url)

			if response_obj.status_code == 200:
				json.dump(response_obj.json(),open(const_USER_JSON(device_id),"w"))
				return True
			else:
				print("[USER ERROR] D/L FAILED FOR %s. TRYING AGAIN!" % (device_id))

	except:
		print("[USER ERROR] GAVE UP D/L FOR %s" % (device_id))
		return False

# checks if a variable is a non empty dictionary
def is_dictionary(some_dict):

	if type(some_dict) == type({}):
		if len(some_dict.keys()) != 0:
			return True

	return False

def get_user_profile_details(device_id):

	json_user_file_name = const_USER_JSON(device_id)

	user_id 	= 0
	user_last_login = 0

	try:
		json_dic = json.load(open(json_user_file_name, 'r'))

		user_id 	= json_dic["profile"]["id"]
		user_last_login = json_dic["profile"]["last_login"]
	except:
		# keeping a track of files which apparently have been downloaded
		# but don't have any data inside it OR are incorrect JSON files
		with open(const_ERROR_FILE(),'a') as fp_ef:
			error_str='[!MISS] {}\n'.format(device_id)
			fp_ef.write(error_str)

		return "<ERROR>","<ERROR>" 

	return user_id,user_last_login

# returns integer version of the string ranks
def get_rank_range_integer(rank_range):

	return map(int,rank_range.split("-"))

# calculates rank range from rank page numbers
# if input is 1, output="1-100"
# if input is 2, output="101-200" and so on
def get_rank_range_from_rank_choice(rank_choice):

	num_data_points = const_NUM_DATA_POINT()

	# calculating rank limits
	upper_lim = rank_choice * num_data_points
	lower_lim = upper_lim - (num_data_points - 1)

	rank_range = "%d-%d" % (lower_lim,upper_lim)

	return rank_range

# gets all data for a given player
def get_user_all_data(each_player):

	# from the main rank list, fetching the following details
	user_game_id	= "0"
	user_last_login = "0"
	user_dev_id	= each_player["device"]
	user_name	= each_player["username"]
	user_country	= each_player["country"]
	user_trophy	= each_player["rank"]
	user_leg_trophy	= each_player["legendaryTrophies"]
	clan_score	= "<NO_CLAN>"
	clan_id		= "<NO_CLAN>"
	clan_tag	= "<NO_CLAN>"
	

	# checking if the user belongs to a clan
	if clan_id != None:
		user_profile	= each_player["profile"]
		user_clan	= user_profile["clan"]

		try:
			clan_score	= user_clan["clanScore"]
			clan_id         = user_clan["id"]
			clan_tag        = user_clan["tag"]
		except:
			pass

	if sys.argv[3] == "0":
		# fetching the complete data of the current user from his profile
		# this causes another GET request
		return_val = fetch_data_userid(user_dev_id)

		# checking if fetching user detail was successful
		if return_val == False:
			return False
		else:
			# from the complete data of the user, getting the user ID, legendary trophy and clan score
			user_game_id, user_last_login  = get_user_profile_details(user_dev_id)

	# creating a list for the current user
	data_extract = [user_game_id,user_name,user_dev_id,user_country,clan_tag,clan_id,user_trophy,user_leg_trophy,clan_score,user_last_login]

	return data_extract

# gets all ranks with userID and device ID
def get_ranks(rank_range):
	json_file_name = const_RANK_JSON(rank_range)

	json_dic = json.load(open(json_file_name,'r'))

	# list to store all the data
	l_name_dev = []

	# getting lower limit of the rank range in integer
	lim_cnt = list(get_rank_range_integer(rank_range))[0]

	for each_player in json_dic["ranks"]:

		# gathering a tuple of data for each player 
		data_extract = get_user_all_data(each_player)

		# if a players data could not be fetched, then it's skipped
		if data_extract == False:
			continue

		# adding the player rank in the list
		data_extract.insert(0,lim_cnt)

		# adding the tuple to the main list
		l_name_dev.append(data_extract)
 
		# deleting the user data json file once the work is done
		if sys.argv[3] == "0":

			try:
				os.remove(const_USER_JSON(each_player["device"]))
			except:
				with open(const_ERROR_FILE(),'a') as fp_ef:
					error_str = '[!DELETE] {} | {}\n'.format(lim_cnt,each_player["device"])
					fp_ef.write(error_str)

		lim_cnt += 1

	# writing the list in a csv file
	fp = open(const_CSV_FILE_NAME(rank_range), 'wb')
	wr = csv.writer(fp, delimiter='|')
	wr.writerows(l_name_dev)

	print("[RANK SUCCESS] Players details of %s written to file" % (rank_range))

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

	# removing the json file containing all the details (Information already extracted)
	os.remove(const_RANK_JSON(rank_range))

if __name__ == "__main__":
	main()
