#!/usr/bin/python

import json
import requests
import os
import datetime
import subprocess
import time
from datetime import timedelta

webhook_url = 'https://hooks.slack.com/services/XXXX/XXXX/XXXX'
slack_channel = 'some_slack_channel'
slack_username = 'sync_bot'
rsync_user = 'some_user'
rsync_host = 'some_hostname'
from_path = '/path/on/rsync_host/you/want/to/sync'
save_path = '/path/on/current_host/you/want/to/sync/to'
log_path = '/some/path/to/some_log.log'


def notify_slack_channel(url, channel, user, fallback, title, text, color, emoji):
    headers = {'content-type':'application/json'}
    payload = json.dumps({
            "channel": channel,
            "username": user,
            "attachments": [
                {
                    "fallback": fallback,
                    "title": title,
                    "text": text,
                    "color": color
                }
            ],
            "icon_emoji": emoji,
    })
    # print(payload)
    request = requests.post(url, headers=headers, data=payload)
    print "Response: %s - %s" % (request.status_code, request.reason)

# Removed method. Might be useful later so I'm leaving it here.
def read_log():
    try:
        with open (log_path, "r") as myfile:
            data = myfile.read()
            exitcode = 0
    except:
        data = "ERROR: Log file was unreadable."
        exitcode = 1
    return (data, exitcode)

def rsync():
    # Delete old log file, I only store the current run results
    if os.path.isfile(log_path):
        os.remove(log_path)

    cmd = ['/usr/bin/rsync', '--human-readable', '--archive', '--compress', '--no-p', '--no-g', 
        '--chmod=ugo=rwX', '--delete-before', rsync_user+'@'+rsync_host+':'+from_path, save_path, 
        '--log-file='+log_path, '--stats']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    exitcode = proc.returncode
    return (output, unused_error, exitcode)
        

def main():
    start_time = time.time()
    output, unused_error, exitcode = rsync()
    end_time = time.time()
    log = output
    duration = "Duration: %s" % timedelta(seconds=end_time - start_time)
    
    # Set colors for good or error
    if exitcode == 0:
        color = "good"
    else:
        color = "danger"

    # Format Slack Message
    fallback = 'NEW: Sync Log Available'
    title = 'Sync Log'
    text = "%s \n %s" % (duration, log)
    emoji = ''
    notify_slack_channel(webhook_url, slack_channel, slack_username, fallback, title, text, color, emoji)

if __name__ == '__main__':
    main()