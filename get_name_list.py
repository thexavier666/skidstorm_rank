#!/usr/bin/python3

import json
import requests
import sys
import os			# for deleting user json files
import unicodecsv as csv	# for writing spl. characters into file in UNICODE
import logging

########## ARGUMENTS ###########

# argument 1 = numeric | which rank page to fetch
# argument 2 = numeric | in which folder to keep the collected data
# argument 3 = binary  | 0 : default fetch, 1 : don't fetch user ID, fetches are much faster

########## CONSTANTS ###########

# number of player entries to be fetched in one go
def const_NUM_DATA_POINT():
	return 250

# location where the data is to stored
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
	return "%serror_list.log" % (const_DATA_DIR())

########## LOGGING ##################

def set_logging_params(error_file_name):
	logging.basicConfig(filename=error_file_name,
	format='%(levelname)s | %(asctime)s | %(message)s',
	datefmt='%m/%d/%Y %I:%M:%S %p',
	level=logging.INFO)

def print_and_log(error_str):
	print(error_str)
	logging.info(error_str)

#####################################

# fetches all data from main rank
def fetch_data_all(rank_range):
	ss_ip = const_SS_IP()
	ss_url = const_SS_URL_FORMAT()

	full_url = ss_url % (ss_ip, rank_range)

	try:
		while True:
			response_obj = requests.get(full_url)

			if response_obj.status_code == 200:
				json.dump(response_obj.json(),open(const_RANK_JSON(rank_range),"w"))
				print("RANK SUCCESS : FETCH FOR RANGE %s FINISHED" % (rank_range))

				return True
			else:
				print("RANK ERROR : TRYING AGAIN FOR %s" % (rank_range))
	except:
		error_str = 'RANK D/L FAILED : {}'.format(rank_range)
		print_and_log(error_str)

		return False

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
				print()
				error_str = "USER ERROR : TRYING AGAIN FOR {}".format(device_id)
				print_and_log(error_str)

	except:
		error_str = 'USER D/L FAILED : {} : FILE STATUS {}'.format(device_id,os.path.isfile(const_USER_JSON(device_id)))
		print_and_log(error_str)

		return False

# checks if a variable is a non empty dictionary
def is_dictionary(some_dict):

	if type(some_dict) == type({}):
		if len(some_dict.keys()) != 0:
			return True

	return False

# extracts data for a given user
def get_user_profile_details(device_id):

	json_user_file_name = const_USER_JSON(device_id)

	user_id         = 0
	user_init_login = 0
	user_last_login = 0
	user_play_dur   = 0
	user_game_played= 0
	user_game_wins  = 0
	user_maxrank    = 0
	user_vip_level  = 0
	user_vip_exp    = 0
	user_diamonds   = 0
	user_coins      = 0
	user_gas        = 0

	try:
		json_dic        = json.load(open(json_user_file_name, 'r'))

		user_id         = json_dic["profile"]["id"]
		user_init_login = json_dic["profile"]["created"]
		user_last_login = json_dic["profile"]["last_login"]
		user_play_dur   = json_dic["profile"]["profile"]["timePlayed"]
		user_game_played= json_dic["profile"]["gamesPlayed"]
		user_game_wins  = json_dic["profile"]["wins"]
		user_maxrank    = json_dic["profile"]["economy"]["maxRank"]
		user_vip_level  = json_dic["profile"]["economy"]["vipInfo"]["vipMaxLevel"]
		user_vip_exp    = json_dic["profile"]["economy"]["vipInfo"]["vipExp"]
		user_diamonds   = json_dic["profile"]["economy"]["diamonds"]
		user_coins      = json_dic["profile"]["economy"]["coins"]
		user_gas        = json_dic["profile"]["economy"]["gasolineBucket"]

	except:
		# keeping a track of files which apparently have been downloaded
		# but don't have any data inside it OR are incorrect JSON files

		error_str='FILE OPEN ERROR : {}'.format(device_id)
		print_and_log(error_str)

		return False,False

	return [user_id, user_init_login, user_last_login, user_play_dur, 
                user_game_played, user_game_wins, user_maxrank, 
                user_vip_level,user_vip_exp, user_diamonds, user_coins, user_gas]

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

	rank_range = "{}-{}".format(lower_lim,upper_lim)

	return rank_range

# gets all data for a given player
def get_user_all_data(each_player):

	# from the main rank list, fetching the following details
	user_dev_id		= each_player["device"]
	user_name		= each_player["username"]
	user_country            = each_player["country"]
	user_trophy		= each_player["rank"]
	user_leg_trophy	= each_player["legendaryTrophies"]
	clan_score		= "<NO_CLAN>"
	clan_id			= "<NO_CLAN>"
	clan_tag		= "<NO_CLAN>"

	data_extract = []
	user_profile_data = [0]

	# checking if the user belongs to a clan
	if clan_id != None:
		user_clan = each_player["profile"]["clan"]

		try:
			clan_score	= user_clan["clanScore"]
			clan_id		= user_clan["id"]
			clan_tag	= user_clan["tag"]
		except:
			pass

	# no need to return any profile specific data
	data_extract = [user_name,user_dev_id,
                user_country,clan_tag,clan_id,
                user_trophy,user_leg_trophy,clan_score]

	if sys.argv[3] == "0":
		# fetching the complete data of the current user from his profile
		# this causes another GET request
		return_val = fetch_data_userid(user_dev_id)

		# checking if fetching user detail was successful
		if return_val == False:
			return False
		else:
			# getting the data which is only available in the user profile
			user_profile_data = get_user_profile_details(user_dev_id)

			if user_profile_data[0] == False:
				return False
			else:
				# inserting user ID in the beginning
				data_extract.insert(0,user_profile_data[0])

				# inserting rest of the data at the end
				data_extract += user_profile_data[1:]

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
		if data_extract != False:

			# adding the player rank in the list
			data_extract.insert(0,lim_cnt)

			# adding the tuple to the main list
			l_name_dev.append(data_extract)
	 
			# deleting the user data json file once the work is done
			if sys.argv[3] == "0":

				try:
					os.remove(const_USER_JSON(each_player["device"]))
				except:
					error_str = 'FILE DELETE FAILED : {} : {}'.format(each_player["device"], lim_cnt)
					print_and_log(error_str)

		# it indicates the current rank of the player
		lim_cnt += 1

	# writing the list in a csv file
	fp = open(const_CSV_FILE_NAME(rank_range), 'wb')
	wr = csv.writer(fp, delimiter='|')
	wr.writerows(l_name_dev)

	print("RANK SUCCESS : DETAILS OF %s SAVED" % (rank_range))

def main():

	set_logging_params(const_ERROR_FILE())

	# input = 1 means rank 1-100
	# input = 2 means rank 101-200 and so on
	rank_choice = int(sys.argv[1])

	# getting rank range based on input from user
	rank_range = get_rank_range_from_rank_choice(rank_choice)

	# fetches complete rank data from Skidstorm Servers
	ret_val = fetch_data_all(rank_range)

	if ret_val != False:
		# extracting data from json
		get_ranks(rank_range)

		# removing the json file containing all the details (Information already extracted)
		os.remove(const_RANK_JSON(rank_range))

	else:
		error_str = 'RANK ERROR : FILE MISSING {}'.format(rank_range)
		print_and_log(error_str)

if __name__ == "__main__":
	main()
