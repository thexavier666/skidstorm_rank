cat $1 | cut -d',' -f 5,6,9 | sort -u -k1,1 -t',' | sort -k3 -n -t',' -r | column -s',' -t | head -n $2 
