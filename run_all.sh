#!/bin/bash

# number of rank pages to be fetched
num_pages=$1

# directory number where data will be stored
data_num=$2

# creating directory to store all data
mkdir "data_${data_num}"

for (( i=1; i<=$num_pages; i++ ))
do
	python3 get_name_list.py $i $data_num &
done

echo "ALL FETCH STARTED!"
