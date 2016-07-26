#!/bin/bash -x
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
echo "$n_size"
let "c_num=$n_bs * 2 - 1"


num=$(grep "nsze" nvme_ns_log | awk '{print $3}')
((num_10=$num))
echo $num_10

# If you do not want to write the whole disk, use num_tmp in the for loop
let "num_tmp=$num_10 / 2"
echo $num_tmp

let "step_num=$n_bs * 2"

echo "wr_sector_'$n_bs'k"

time_log="time_log_read_sequential""$n_bs"
if [ -f "$time_log" ];then
    rm -f $time_log
fi

echo "whole read begins at:" > $time_log
date >> $time_log

for ((i=0;i<"$num_tmp";i+=$step_num))
do  
    let "num=$i + $step_num"
    if [[ "$num" -ge "$num_10" ]];then
        echo "number out of range..."
	echo "error lba range"
	date >> $time_log
	exit 1
    fi
    nvme read /dev/nvme0n1 -s $i -c $c_num -z "$n_size" -d rd_sector_"$n_bs"k
    if [[ "$?" -ne 0 ]];then
        echo "nvme read command failed........"
	echo "error read" >> $time_log
	date >> $time_log
        exit 1
    fi
done
echo "whole read ends at:" >> $time_log
date >> $time_log
