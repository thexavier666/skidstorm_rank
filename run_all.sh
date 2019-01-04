#!/bin/bash
num_pages=$1
for (( i=1; i<=$num_pages; i++ ))
do
	python get_name_list.py $i &
done

echo "ALL FETCH STARTED!"
