#!/usr/bin/python

a = ["[global]\nioengine=libaio\niodepth=100\ndirect=1\nloops=1000\nruntime=600\nsize=600G\nfilename=tmp_test/io.tst\ngroup_reporting\n[rr-0]\nbs=4k\nrw=randread\nnumjobs=20\nthread\n[sw-0]\nbs=256k\nrw=write\nrate_iops=80\nrefill_buffers\n" , \
                "[global]\nbs=4k\nioengine=libaio\niodepth=100\ndirect=1\nloops=1000\nruntime=600\n[randrw-0]\nrw=randrw\nsize=600G\nrwmixread=10\nfilename=tmp_test/io.tst\nrefill_buffers\ngroup_reporting\n" ,\
                "[global]\nbs=4k\nioengine=libaio\niodepth=100\ndirect=1\nloops=1000\nruntime=600\n[randrw-0]\nrw=randrw\nsize=600G\nrwmixread=50\nfilename=tmp_test/io.tst\nrefill_buffers\ngroup_reporting\n" ,\
                "[global]\nbs=4k\nioengine=libaio\niodepth=100\ndirect=1\nloops=1000\nruntime=600\n[randrw-0]\nrw=randrw\nsize=600G\nrwmixread=90\nfilename=tmp_test/io.tst\nrefill_buffers\ngroup_reporting\n" ,\
                "[global]\nbs=4k\nioengine=sync\niodepth=1\ndirect=1\nloops=1000\nsize=600G\nruntime=600\ngroup_reporting\nrefill_buffers\nthread\n[randrw4k]\nrw=randrw\nrwmixread=66\nfilename=tmp_test/io.tst\nnumjobs=1\n" ,\
                "[global]\nbs=4k\nioengine=sync\niodepth=1\ndirect=1\nloops=1000\nsize=600G\nruntime=600\ngroup_reporting\nrefill_buffers\nthread\n[randrw4k]\nrw=randrw\nrwmixread=55\nfilename=tmp_test/io.tst\nnumjobs=1\n" ,\
                "[global]\nbs=4k\nioengine=sync\niodepth=1\ndirect=1\nloops=1000\nsize=600G\nruntime=600\ngroup_reporting\nrefill_buffers\nthread\n[randrw4k]\nrw=randrw\nrwmixread=66\nfilename=tmp_test/io.tst\nnumjobs=2\n" ,\
                "[global]\nbs=4k\nioengine=sync\niodepth=1\ndirect=1\nloops=1000\nsize=600G\nruntime=600\ngroup_reporting\nrefill_buffers\nthread\n[randrw4k]\nrw=randrw\nrwmixread=55\nfilename=tmp_test/io.tst\nnumjobs=2\n" ]

for i in a:
    print i

case_name = ["20MBPSsw256k","1rr9rw","5rr5rw","9rr1rw","2rr1rw_1thread_mysql","5rr4rw_1thread_mysql","2rr1rw_2thread_mysql","5rr4rw_2thread_mysql"]

