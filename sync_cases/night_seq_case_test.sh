#!/bin/bash -x
OUTPUT="night_out"
function run_test {
    $* |  >> ${OUTPUT} 2>&1
    if (( $? )); then
        echo ${red}"FAILED!"${rst}
        echo "Failed running command: "
        echo  "   $*"
        exit 1
    fi
}

run_test /bin/bash read_write_sync.sh -n 8
#run_test bash read_write_sync.sh -n 16
#run_test bash read_write_sync.sh -n 32
#run_test bash read_write_sync.sh -n 64
#run_test bash read_write_sync.sh -n 128
