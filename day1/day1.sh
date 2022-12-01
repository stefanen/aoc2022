../../p_data.sh 1 | awk '"" == $1 {print s;s=0} {s=s+$1} END {print s}' | sort -n | tail -n 1
../../p_data.sh 1 | awk '"" == $1 {print s;s=0} {s=s+$1} END {print s}' | sort -n | tail -n 3 | paste -sd+ | bc
