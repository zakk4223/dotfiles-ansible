#!/bin/bash

set -e
set -o pipefail

export ARCH=arm
export LOCALVERSION=-MiSTer
export INSTALL_MOD_PATH=./modules-mister

export CROSS_COMPILE=/home/zakk/Downloads/gcc-arm-10.2-2020.11-x86_64-arm-none-linux-gnueabihf/bin/arm-none-linux-gnueabihf-

make -j$(nproc) $@

