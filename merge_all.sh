#!/bin/bash

# number of pages fetched
num_pages=$1

# the index of the data to be fetched
data_index=$2

data_dir="data_${data_index}/"
master_db_file_name="${data_dir}master_db.csv"

touch $master_db_file_name

num_data_point=100

for (( i=1; i<=$num_pages; i++ ))
do
	upper_lim=$((i*num_data_point))
	lower_lim=$((upper_lim-(num_data_point-1)))

	file_name="${data_dir}user_id_${lower_lim}-${upper_lim}.csv"
	cat $file_name >> $master_db_file_name
done
