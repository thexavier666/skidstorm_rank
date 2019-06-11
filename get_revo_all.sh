#!/bin/bash

data_folder_id=$1
revo_team_file=$2

clan_list=(
	'REVO,93633'
	'REV0,119234'
	'RΕVO,123276'
	'RЕV0,130058'
	'REVΟ,126321'
)

for i in ${clan_list[@]}; do
	echo ${i}
	grep ${i}  data_${data_folder_id}/master_db.csv | cut -d, -f 2,4,6 | head -n 20 | sort -n -t , -k 2 >> ${revo_team_file}
done
