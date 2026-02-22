#!/usr/bin/env python3

import sys


with open(sys.argv[1], 'rb') as f:
    with open(sys.argv[2], 'wb') as nf:
        while True:
            new_byte = f.read(1)
            if not new_byte:
                break
            nf.write(ord(new_byte).to_bytes(1))
            nf.write(int(0).to_bytes(1))
