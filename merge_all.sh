#!/bin/bash
master_db_file_name="master_db.csv"

touch $master_db_file_name

num_pages=$1

for (( i=1; i<=$num_pages; i++ ))
do
	upper_lim=$((i*100))
	lower_lim=$((upper_lim-99))

	file_name="user_id_$lower_lim-$upper_lim.csv"
	cat $file_name >> $master_db_file_name
done
