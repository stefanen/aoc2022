cat input_d_25.txt | awk '{$1=$0;$2=$0;gsub(/=/,0,$1);gsub(/-/,0,$1);gsub(/1/,0,$2);gsub(/2/,0,$2);gsub(/=/,2,$2);gsub(/-/,1,$2); print $1"-"$2}' | paste -sd+ | echo "ibase=5;obase=5;$(cat -)" | bc | sed -e 's/./&\n/g' | tac | awk '/[0-9]/ {if (carry+$0<3) {print carry+$0;carry=0} else {print -5+(carry+$0); carry=1}}' | tac | sed -e 's/-2/=/' -e 's/-1/-/' | tr -d "\n" && echo