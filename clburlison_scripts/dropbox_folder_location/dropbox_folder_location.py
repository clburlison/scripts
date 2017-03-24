#!/usr/bin/python
"""H/t to eholtam for posting in slack"""

import json
import os

print("Personal: ")
f = open(os.path.expanduser('~/.dropbox/info.json'), 'r').read()
data = json.loads(f)
print(data.get('personal', {}).get('path', '').replace('', 'None'))

print("Business: ")
f = open(os.path.expanduser('~/.dropbox/info.json'), 'r').read()
data = json.loads(f)
print(data.get('business', {}).get('path', '').replace('', 'None'))
