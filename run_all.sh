#!/bin/bash

num_pages=$1
data_num=$2

for (( i=1; i<=$num_pages; i++ ))
do
	python get_name_list.py $i $data_num &
done

echo "ALL FETCH STARTED!"
