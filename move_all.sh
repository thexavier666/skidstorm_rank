#!/bin/bash
mkdir data_$1
./merge_all.sh
mv all_rank* data_$1
mv user_id* data_$1
mv master_db.csv data_$1