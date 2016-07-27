#!/bin/bash 

nvme id-ns /dev/nvme0 -n 1 > nvme_ns_log
#nvme format /dev/nvme0 -n 1 -l 0
num=$(grep "nsze" nvme_ns_log | awk '{print $3}')
echo $num
((num_10=$num))
echo $num_10
declare -a array_origin1
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


let "step_num=$n_bs *2"
let "upper_num_for=$num_10 - $step_num"

echo "$upper_num_for"

# Divide disk_size to 10 parts. save 10 number array.
declare -a loop_num
let "upper_num_average=$upper_num_for / 10"

for i in {1..10}
do  
    echo "${upper_num_average}"
    echo "$i"
    let "loop_num[$i]=$upper_num_average * $i"
done 
echo -e "10 averaged loop array:\n"
echo "${loop_num[@]}"
     

# Following part generate each random array.
#for ((i=0;i<"$upper_num_for";i+="$step_num"))
for ((i=0;i<4096;i+="$step_num"))
do
    flag=1
    while [ "$flag" -eq 1 ]
        do
	    rand_int=$(rand 0 "upper_num_for")
	    if [[ "$i" -eq 0 ]];then
                array_origin1=(${array_origin1[*]} $rand_int)
		flag=0
            elif [[ "${array_origin1[@]}" =~ $rand_int ]];then
		break
	    else
		array_origin1=(${array_origin1[*]} $rand_int)
		flag=0
	    fi
		
	done
done

array_len=${#array_origin1[@]}
let "array_len=array_len - 1"
echo "$array_len"
echo "${array_origin1[@]}"

# Save the array numbers to a file, one number occupies a line
for i in `seq $array_len`
do
   let "j=$i - 1"
   echo "$j"
   echo "${array_origin1[$j]}"
   if [ "$j" -eq 0 ];then
       echo "${array_origin1[$j]}" > random_array.bak
   else
       echo "${array_origin1[$j]}" >> random_array.bak
   fi
done


line_num=`awk 'END{print NR}' random_array.bak`

echo "$line_num"

cat random_array.bak
cp  random_array.bak random_array

# Read the number file, save the numbers to an array
for i in `seq $line_num`
do
   let "j=$i - 1"
   array_origin[$j]=$(head -1 random_array.bak)
   sed -i '1d' random_array.bak
   echo "$j"
   echo "${array_origin[$j]}"
done
#
echo "******************************************"
array_len=${#array_origin[@]}


echo "length of the arry_origin:"
echo $array_len
echo -e "The total array_origin:\n"
echo "${array_origin[@]}"



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
