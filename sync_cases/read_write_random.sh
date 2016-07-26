#!/bin/bash  -x
nvme id-ns /dev/nvme0 -n 1 > nvme_ns_log
nvme format /dev/nvme0 -n 1 -l 0
num=$(grep "nsze" nvme_ns_log | awk '{print $3}')
echo $num
((num_10=$num))
echo $num_10
declare -a array_origin

# which kind of size do you want to run ---> eg. 8k, -n 8
while getopts ":n:" opt
do
    case $opt in
        n) echo "++++++++++++++++"
	   echo "$OPTARG"
	   n_bs=$OPTARG;;
	?) echo "error"
	   exit 1;;
    esac
done

let "n_size=$n_bs * 1024"
let "c_num=$n_bs * 2 - 1"

dd if=/dev/urandom of=wr_sector_"$n_bs"k bs="$n_size" count=1

# define random number generation function
function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(date +%s%N)
    echo $(($num%$max+$min))
}


let "step_num=$n_bs *2 "
let "upper_num=$n_size / $step_num"
let "upper_num_for=$upper_num - $step_num"

#for ((i=0;i<"$upper_num_for";i+="$step_num"))
for ((i=0;i<4096;i+="$step_num"))
do
    array_len1=${#array_origin[@]}
    while [ "$array_len1" -eq $i ]
        do
	    rand_int=$(rand 0 "$upper_num")
	    if [[ "$i" -eq 0 ]];then
                array_origin=(${array_origin[*]} $rand_int)
                array_len1=${#array_origin[@]}
            elif [[ "${array_origin[@]}" =~ $rand_int ]];then
		continue
	    else
		array_origin=(${array_origin[*]} $rand_int)
                array_len1=${#array_origin[@]}
	    fi
		
	done
done

for i in "${!array_origin[@]}"
do  
    let "array_origin[$i]=${array_origin[$i]} * $step_num"

done

echo ${array_origin[*]} > random_array.bak
array_len=${#array_origin[@]}
echo "length of the arry_origin:"
echo $array_len

time_log="time_log_""$n_bs"
if [ -f "$time_log" ];then
    rm -f "$time_log"
fi

# do nvme read write command test
echo "Test begins at ...:" > "$time_log"
date >> "$time_log"
for ((i=0;i<"$array_len";i++))
do
    if [[ "$i" -ge "$num_10" ]];then
        echo "number out of range..." >> "$time_log"
	date >> "$time_log"
	exit 1
	
    fi
    nvme write /dev/nvme0n1 -s ${array_origin[$i]} -c $c_num -z $n_size -d wr_sector_"$n_bs"k
    if [[ "$?" -ne 0 ]];then
        echo "nvme write command failed........" >> "$time_log"
	date >> "$time_log"
        exit 1
    fi
    nvme read /dev/nvme0n1 -s ${array_origin[$i]} -c $c_num -z $n_size -d rd_sector_"$n_bs"k
    if [[ "$?" -ne 0 ]];then
        echo "nvme read command failed........" >> "$time_log"
	date >> "$time_log"
        exit 1
    fi
    diff wr_sector_"$n_bs"k rd_sector_"$n_bs"k
    if [[ "$?" -ne 0 ]];then
        echo "diff command failed........"
	echo "error lba number:" >> "$time_log"
	echo "${array_origin[$i]}"
	date >> "$time_log"
        exit 1
    fi
    
done
echo "Test ends at...:" >> "$time_log"
date >> "$time_log"
