#!/usr/bin/python
import subprocess
import argparse
import conf
import os
import sys


def do_compare(nvme_cmd, old_result):
    # Read the old nvme cmd result to list & str
    if os.path.exists(old_result):
        f = open(old_result, 'r')
        old_result_list = f.readlines()
        f.close()
        #tmp_result_str = " ".join(old_result_content)
    else:
	print "old result file not found in the current dir, please check it!!!"
	sys.exit()


    # Call nvme cmd, then compare the two result files, print the difference 
    p = subprocess.Popen([ nvme_cmd ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    new_result_list = p.communicate()[0]
    diff_result = [ i for i in old_result_list if i not in new_result_list ]
    if len(diff_result) == 0:
        print "The same, no difference.\n"
    else:
        print "============================================================="
        print "The different result:\n"
        diff_result_str = " ".join(diff_result)
        print diff_result_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='device', type=str, help='target SSD eg. sda', required=True)
    parser.add_argument('-c', choices=('id-ns', 'id-ctrl', 'get feature', 'set feature', 'fmware dld', 'fmware cmmmit'), dest='nvme_cmd', type=str, help='choose nvme_cmd from given list', action='store', required=True)
    parser.add_argument('-args', dest='extra_args', nargs= '+', help='extra_args of the nvme cmd, remember to use "" to include it')
    parser.add_argument('-f', dest='old_result', type=str, help='old result file name that needs to be compared', required=True)
    args = parser.parse_args()
    cmd_list = []
    cmd_list.append(conf.cmd_dict[args.nvme_cmd])
    cmd_list.append(args.device)
    if args.extra_args:
	cmd_list = cmd_list + args.extra_args
    cmd = " ".join(cmd_list)
    do_compare(cmd, args.old_result)
