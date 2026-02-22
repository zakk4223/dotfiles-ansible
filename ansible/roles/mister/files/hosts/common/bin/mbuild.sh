#!/bin/bash

# create simple text file named 'host' in this folder with IP address of your MiSTer.

if [ -z "$HOST" ]
then
  HOST=mister
  [ -f host ] && HOST=$(cat host)
fi

if [[ "$1" == "debug" ]]
then
  export DEBUG=1
fi
# make script fail if any command failed,
# so we don't need to check the exit status of every command.
set -e
set -o pipefail
#docker run -it --rm -v "$(pwd)":/mister -w /mister theypsilon/gcc-arm:10.2-2020.11 make -j12
PATH=/home/zakk/Downloads/gcc-arm-10.2-2020.11-x86_64-arm-none-linux-gnueabihf/bin:$PATH make -j16
#PATH=/home/zakk/Downloads/gcc-arm-10.3-2021.07-x86_64-arm-none-linux-gnueabihf/bin:$PATH make -j16


set +e
plink root@$HOST -pw 1 -no-antispoof 'killall MiSTer'

COPYBIN="bin/MiSTer"
if [[ "$1" == "debug" ]]
then
  COPYBIN="bin/MiSTer.elf"
fi
set -e
ftp -n <<EOF
open $HOST
user root 1
binary
put $COPYBIN /media/fat/MiSTer_dev
EOF

if [[ "$1" == "debug" ]] 
then
	plink root@$HOST -t -pw 1 -no-antispoof 'sync;PATH=/media/fat:$PATH;gdb MiSTer_dev'
else
	plink root@$HOST -t -pw 1 -no-antispoof 'sync;PATH=/media/fat:$PATH;MiSTer_dev'
fi

