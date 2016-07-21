#!/usr/bin/python
import argparse
import subprocess
import conf

def do_parse(nvme_cmd, device):
    cmd = conf.cmd_dict[nvme_cmd]
    p = subprocess.Popen(['%s %s' % (cmd, device)], stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    subprocess.Popen('touch id_ctrl_out', stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    f = open('id_ctrl_out', 'w')
    f.write(p.communicate()[0])
    f.close()
    f = open('id_ctrl_out', 'r')
    id_ctrl_content = f.readlines()
    f.close()

    # delete the first line 'NVME Identify Controller'
    del id_ctrl_content[0]
    # remove the '\n' in each line
    id_ctrl_content = [ i.strip('\n') for i in id_ctrl_content ]

    # combine the last two lines of the cmd output
    tmp_content = id_ctrl_content[-1]
    del id_ctrl_content[-1]
    id_ctrl_content[-1] = id_ctrl_content[-1] + tmp_content
    
    # create the dict
    id_ctrl_content = [ i.split(' :') for i in id_ctrl_content ]
    id_ctrl_dict = dict(id_ctrl_content)

    # remove blank space of each item in the dict
    key_list = id_ctrl_dict.keys()
    value_list = id_ctrl_dict.values()
    key_list = [ i.strip() for i in key_list ] 
    value_list = [ i.strip() for i in value_list ]
    id_ctrl_dict = dict(zip(key_list, value_list))
    
    # process the last line
    last_value = id_ctrl_dict['ps    0']
    last_tmp_list = last_value.split()
    last_tmp_list = [ i.split(":") for i in last_tmp_list ]
    last_tmp_list[0][1] = last_tmp_list[0][1] + ' ' + last_tmp_list[1][0]
    del last_tmp_list[1:]

    ####### As for mp:25.00W operational, only remain "mp：25.00W", remaining all deleted#####
    
    # Update the value of 'ps    0'
    last_tmp_dict = dict(last_tmp_list)
    id_ctrl_dict['ps    0'] = last_tmp_dict

    print "==================================="
    print "The final dict ...........\n"
    print id_ctrl_dict
    print "\n==================================="

   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='device', type=str, help='target SSD eg. sda', required=True)
    parser.add_argument('-c', choices=('id-ns', 'id-ctrl', 'get feature', 'set feature', 'fmware dld', 'fmware cmmmit'), dest='nvme_cmd', type=str, help='choose nvme_cmd from given list', action='store', required=True)
    args = parser.parse_args()
    do_parse(args.nvme_cmd, args.device)
