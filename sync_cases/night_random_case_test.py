#!/usr/bin/python
import os

#bs_list = [ '4', '8', '16', '32', '64', '128' ]
bs_list = [ '4' ]

for i in bs_list:
    cmd = "bash read_write_sync.sh -n %s" % i
    print "running %sk read and write case:\n"
    os.system(cmd)
    
