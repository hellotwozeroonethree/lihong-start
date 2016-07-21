#!/usr/bin/python
import subprocess
import sys
import conf
import argparse


def do_parse(nvme_cmd, device):
    cmd = conf.cmd_dict[nvme_cmd]
    p = subprocess.Popen(['%s %s -n 1' % (cmd, device)], stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    subprocess.Popen('touch nvme_ns_out', stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    f = open('nvme_ns_out', 'w')
    f.write(p.communicate()[0])
    f.close()
    f = open('nvme_ns_out', 'r')
    nvme_ns_content = f.readlines()
    f.close()
    # delete the first line "NVME Identify Namespece *"
    del nvme_ns_content[0]
    # remove the '\n' in each line
    nvme_ns_content = [ i.strip('\n') for i in nvme_ns_content ]
    # create initial dict, a (key, value) correspond to a line
    nvme_ns_content = [ i.split(' :') for i in nvme_ns_content ]
    nvme_ns_dict = dict(nvme_ns_content)

    # remove the blank space of the dictionary item
    dict_key = nvme_ns_dict.keys()
    dict_value = nvme_ns_dict.values()
    dict_key = [ i.strip() for i in dict_key ]
    dict_value = [ i.strip() for i in dict_value ]
    nvme_ns_dict = dict(zip(dict_key, dict_value))

    # parse the "(in use)" line, put the required data 'ms, ds, rp' in dict
    for i in range(7):
        key = 'lbaf  ' + str(i)
        value = nvme_ns_dict[key]
        if '(in use)' in value:
	    return_lbaf = key
            nvme_ns_dict[key] = value.strip('(in use)')
	    value_list = nvme_ns_dict[key].split()
	    value_list = [ i.split(':') for i in value_list ]
	    nvme_ns_dict[key] = dict(value_list)

    print "the final total dict is", nvme_ns_dict , "\n"
    print "the return_lbaf is",  return_lbaf , "\n"
    print "the specified (in use) line dict is", nvme_ns_dict[return_lbaf], "\n"
    print "you should know ms", nvme_ns_dict[return_lbaf]['ms'], "\n"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='device', type=str, help='target SSD eg. sda', required=True)
    parser.add_argument('-c', choices=('id-ns', 'id-ctrl', 'get feature', 'set feature', 'fmware dld', 'fmware cmmmit'), dest='nvme_cmd', type=str, help='choose nvme_cmd from given list', action='store', required=True)
    args = parser.parse_args()
    do_parse(args.nvme_cmd, args.device)
   
