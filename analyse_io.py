#!/usr/bin/python

import os
import shutil

result_path = "./result"

def analyse_iostat(filename,dev,rw):
	if "read" in rw:
		cmd = "cat %s | grep %s | awk {'print $4'}" %(filename, dev)
	elif "write" in rw:
		cmd = "cat %s | grep %s | awk {'print $5'}" %(filename, dev)

	fd = os.popen(cmd)
	con = fd.read()
	fd.close()

	cmd1 = "cat %s | grep %s | awk {'print $11'}" %(filename, dev)
	fd1 = os.popen(cmd1)
	con1 = fd1.read()
	fd1.close()

	filename1 = os.path.split(filename)[-1]
	first = 1
	count = 0
	min = 100000000.00
	min_count = 0
	total = 0
	zero_count = 1
	for line in con.split("\n"): #cal r/w
		if not line.strip():
			continue
		if first == 1:
			first = 0
			continue
		
		if zero_count == 1:
			if float(line.strip()) > 0.0:
				zero_count = 0
			else:
				continue 
		
		if float(min) > float(line.strip()):
			min = float(line.strip())

		total = total + float(line.strip())
		count = count + 1

		if float(line.strip()) < 100:
			min_count = min_count + 1

	svctm_1ms = 0
	svctm_max = 0
	first = 1
	zero_count = 1
	for line in con1.split("\n"): #cal svctm
		if not line.strip():
			continue
		if first == 1:
			first = 0
			continue
		if zero_count == 1:
			if float(line.strip()) > 0.0:
				zero_count = 0
			else:
				continue

		if float(svctm_max) < float(line.strip()):
			svctm_max = float(line.strip())

		if float(line.strip()) > 1.0:
			svctm_1ms = svctm_1ms + 1
	
	avg = float(total)/float(count)
	svctm_more_1ms = float(svctm_1ms) / float(count)
	write_line = "%s\t%s\t%s\t%s\t%s\t%s\n" %(filename1, rw, str(avg), str(min), str(min_count), str(count))
	write_file = result_path + "/io_result.csv"
	fd = open(write_file, "a")
	fd.write(write_line)
	fd.close()


if os.path.exists(result_path):
    shutil.rmtree(result_path)

cmd = "mkdir result"
os.system(cmd)
cmd = "touch %s/io_result.csv" % result_path
os.system(cmd)
write_line = "filename\trw\tavg_iops\tmin_iops\tless_than_100_count\ttotal_count\n"
write_file = result_path + "/io_result.csv"
fd = open(write_file, "a")
fd.write(write_line)
fd.close()
analyse_ioresult(filename, dev, rw)
