## Fetching Skidstorm Player Database

### How to run

1. To fetch the complete data, run the following command. The argument `number of pages` must be an integer. If you enter 10, it means 10 pages of data will be fetched where each page contains 100 players, thus the data of 1000 players will be fetched
	```
	./run_all <number of pages>
	```

2. To merge all the data, run the following command. A single file is created which is called `master_db.csv. Make sure the argument value matches the one in the above command

	```
	./merge_all <number of pages>
	```

### Bugs

* To do
