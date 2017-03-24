#!/usr/bin/python

import json, os, pprint

f = open(os.path.expanduser('~/.dropbox/info.json'), 'r').read()
data = json.loads(f)

# To list all dropbox data
pprint.pprint(data)
print('')

# Or to find just the paths
for i in ['personal', 'business']:
    print('{}:'.format(i.capitalize()))
    print(data.get(i, {}).get('path', ''))
