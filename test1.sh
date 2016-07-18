#!/bin/bash
array2=(1 3 5 6 8)
for i in "${!array2[@]}"
do  
   #let "array2[$i]=${array2[$i]} + 2"
   array2[$i]=$(expr "${array2[$i]}" + 2)
done
echo ${array2[@]}

