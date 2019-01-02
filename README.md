## Fetching Skidstorm Player Database

### Pre-requisites

* Python 2.7
* Python library `unicodecsv`

### How to run

1. To fetch the complete data, run the following command. The argument `number of pages` must be an integer. If you enter 10, it means 10 pages of data will be fetched where each page contains 100 players, thus the data of 1000 players will be fetched

	```
	./run_all <number of pages>
	```

2. To merge all the data, run the following command. A single file is created which is called `master_db.csv`. Make sure the argument value matches the one in the above command

	```
	./merge_all <number of pages>
	```

3. To move all data to a folder named `data_<number>`, run the following command

	```
	./move_all <number>
	```

### Data collected

In the `master_db.csv` file, each line contains the details of one user. For each user, the following details are collected.

`user ID, username, device ID, country code, clan tag, clan ID, current number of trophies, number of legendary trophies`

### Bugs

* Some issue showing while running the `merge_all`, but not hampering final results
* Sometimes, a connection might timeout. I have not handled it explicityly. Kindly redownload them by seeing which `json` file is missing and then run the `merge_all` script
