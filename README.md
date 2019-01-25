## Fetching Skidstorm Player Database

### Pre-requisites

* Python 2.7
* Python library `unicodecsv`
* Make sure all the scripts are executable

### How to run

1. To fetch the complete data, run the following command. The argument `<number of pages>` must be an integer. If you enter 10, it means 10 pages of data will be fetched where each page contains 100 players, thus the data of 1000 players will be fetched. The argument `<number>` indicates where the file will be saved. If the argument `<number>` is 10, then the file will be saved in `./data_10`

	```
	./run_all <number of pages> <number>
	```

2. To merge all the data, run the following command. A single file is created which is called `master_db.csv`. Make sure the argument values matches the one in the above command

	```
	./merge_all <number of pages> <number>
	```

3. **OPTIONAL** : If you want to see all the name changes of a particular player, then get the player's game ID, say `<ID>`. Then run this command

	```
	./change_all <ID>
	```

### Data collected

In the `master_db.csv` file, each line contains the details of one user. For each user, the following details are collected.

`user ID, username, device ID, country code, clan tag, clan ID, current number of trophies, number of legendary trophies`

### Files created

* To-do

### Bugs

* [FIXED] Some issue showing while running the `merge_all`, but not hampering final results
* [FIXED] Sometimes, a connection might timeout. I have not handled it explicitly. Kindly redownload them by seeing which `json` file is missing and then run the `merge_all` script
