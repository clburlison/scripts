#!/usr/bin/python
import subprocess

command = ['/usr/bin/curl', '--connect-timeout', '30', 'https://api.ipify.org']

tk = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out, err) = tk.communicate()

print(out)
