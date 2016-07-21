#!/usr/bin/python
import argparse
import subprocess
import random
import os

# cmd_list list admin nvme commands, 'list' item stands for it needs to be add args
cmd_list = [ ["nvme id-ctrl"],
	     ["nvme id-ns", "-n 1"]
	   ]

feature_cmd_list = [ ["nvme get-feature", "-n 1", ["-f", 14]],
	           #  ["nvme set-feature", "-n 1", ["-f", 14]]
                   ]

#format_cmd_list = [ ["nvme format", ["-n"], ["-l"], ["-s", "2"], ["-p", '1'], ["-i", "3"],  ["-m"]]
format_cmd_list = [ ["nvme format", ["-n"], ["-l"],  ["-m"]]]


#Volatile write cache: enable/disable
#nvme set-feature /dev/nvme0 -f 6 -v 1

#Asynchronous Event Configuration
#nvme set-feature /dev/nvme0 -f 0xB -v 1

# set-feature -f [0x1 -- 0xD] -l data_length -d file
# get-log -i [0x1 -- 0x3] -l data_length -d file
# format, identify-ns, read number of ns, read all of lbaf and parameter, for loop format namespace with each lba format.


# Treat feature_cmd_list, add the result to cmd_list
for i in feature_cmd_list:
    head_list = i[:2]
    tmp_list = i[2]
    count = tmp_list[1]
    for j in range(count):
        head_list.append(tmp_list[0] + " " + repr(j))
        cmd_list.append(head_list)
	head_list= i[:2]

        

#Treat format_cmd_list, add the result to cmd_list




def do_test(dev, method, test_loops, result_dir):
    # Prepare result dir
    if os.path.exists(result_dir):
        cmd = "rm -rf %s" % result_dir
	os.system(cmd)
    cmd = "mkdir %s" % result_dir
    os.system(cmd)
    
    # do sequential test
    if method == "sequential":
       print "=================================\n"
       print "You are doing sequential test...."
       for i in range(test_loops):
           for i in cmd_list:
               p = subprocess.Popen([ i ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	       print "*************nvme cmmand output begin**********"
	       print "Command:\n", i
	       print "-----------------------------------------------"
               print p.communicate()[0]
	       content = p.communicate()[0]
	       tmp_list = i.split(' ')
	       file_name = tmp_list[1] + "_" + "log"
	       cmd = "touch %s/%s " % (result_dir, file_name)
	       os.system(cmd)
	       cmd = "echo %s > %s/%s" % (content, result_dir, file_name)
	       os.system(cmd)
	       print "*************nvme command output end***********"

    # do random test
    if method == "random":
       print "=================================\n"
       print "You are doing random test........"
       tmp_count = 0
       if test_loops > len(cmd_list):
           test_loops = len(cmd_list)
       for i in range(test_loops):
	   if i == 0:
	       j = i
	   else:
	       j = random.randint(tmp_count, i)
	       tmp_count = tmp_count + 1
           
           p = subprocess.Popen([ cmd_list[j] ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	   print "*****************nvme command output begin**********"
	   print "Command:\n", cmd_list[j]
	   print "----------------------------------------------------"
           print p.communicate()[0]
	   print "*****************nvme command output end ***********"
	   
	   


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='device', type=str, help='target SSD eg. /dev/nvme0', required=True)
    parser.add_argument('-m', dest='method', type=str, choices=('sequential', 'random'), help='choose running method, sequential or random', required=True)
    parser.add_argument('-n', dest='test_loops', type=int, help='loop number', required=True)
    parser.add_argument('-f', dest='result_dir', type=str, help='dir name, dir to store command running result', required=True)
    args = parser.parse_args()

    # Update cmd_list, add device name
    cmd_list = [ i[0] + " " + args.device + " " + " ".join(i[1:]) for i in cmd_list ]
    print "cmd_list:\n", cmd_list

    do_test(args.device, args.method, args.test_loops, args.result_dir)
