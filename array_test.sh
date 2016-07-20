#!/bin/bash
let "step_num=$n_num * 2"
let "upper_num=$n_size / $step_num"
let "upper_num_=$upper_num - 1"
let "upper_num_step=$upper_num - $step_num"
declare -a array1
for ((i=0;i<$upper_num_step;i+=$step_num))
do
    flag=1
    while [ "$flat" -eq 1 ]
    do
        rand_int=rand(0,$upper_num)
        if [[ "$i" -eq 0 ]];then
            array1=(${array1[*]} randint)
            flag=0
        elif [[ "${array1[@]}" =~ $randint ]];then
            continue
        else
            array1=(${array1[*]} randint)
            flag=0
        fi
    done
done

echo ${array1[@]}

for i in "${!array1[@]}"
do
    array1[$i]=$(expr ${array1[$i]} * $step_num)
done

echo ${array1[@]}

