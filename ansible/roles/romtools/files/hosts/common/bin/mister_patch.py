#!/usr/bin/env python

import sys
from ips_util import Patch


patch = Patch.load(sys.argv[1])

for record in patch.records:
    data = ''
    if 'rle_count' in record:
        data = '{0} x{1}'.format(record['data'].hex(), record['rle_count'])
    else:
        data = " ".join(["{:02x}".format(x) for x in record['data']])

    print('<patch offset="0x{0:06x}">{1}</patch>'.format(record['address'], data))

