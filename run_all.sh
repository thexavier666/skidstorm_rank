#!/bin/bash

# number of rank pages to be fetched
num_pages=$1

# directory number where data will be stored
data_num=$2

# fetch player ID or not
fetch_flag=$3

# creating directory to store all data
mkdir "data_${data_num}"

for (( i=1; i<=$num_pages; i++ ))
do
	python3 get_name_list.py $i $data_num $fetch_flag &
	sleep 1
done

echo "ALL FETCH STARTED!"
