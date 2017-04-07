#!/usr/bin/python
"""
Parse user sessions on macOS so we can determine what users logged in/out and
when the event took place.

Author: Clayton Burlison <https://clburlison.com>
"""

import subprocess
import plistlib
import sys
import pprint


def user_session_data():
    """Obtain the user session data from the last command and parse into a
    python list of dictonary items."""
    events = []
    cmd = ['/usr/bin/last']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    for line in output.split('\n'):
       # remove output we don't care about
       if not any(s in line for s in ['wtmp','ttys']):
           # Clean our list by filtering out empty spaces
           line = filter(None, line.split(' '))
           # last will output empty lines so we need to ignore
           if line:
               #print(line)
               type = line[0]  # type is an event (restart/shutdown) or user
               #print(type)
               time = '{} {} {}'.format(line[3],line[4],line[5])
               #print(time)
               event = {'type':type,'time':time}
               events.append(event)
    pprint.pprint(events)
    return events

events = user_session_data()
