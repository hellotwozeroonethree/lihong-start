#!/bin/bash
bash read_write_random.sh -n 8
if [ "$?" -ne 0 ]; then
    echo "8k data read write failed"
fi
bash read_write_random.sh -n 16
if [ "$?" -ne 0 ]; then
    echo "16k data read write failed"
fi
bash read_write_random.sh -n 32
if [ "$?" -ne 0 ]; then
    echo "32k data read write failed"
fi
bash read_write_random.sh -n 64
if [ "$?" -ne 0 ]; then
    echo "64k data read write failed"
fi
bash read_write_random.sh -n 128
if [ "$?" -ne 0 ]; then
    echo "128k data read write failed"
fi
