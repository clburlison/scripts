# -*- coding: utf-8 -*-
# http://stackoverflow.com/a/34325723/4811765

import sys


# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

#
# Sample Usage
#

from time import sleep

# make a list
items = list(range(0, 57))
i = 0
l = len(items)


# Initial call to print 0% progress
print_progress(i, l, prefix='Progress:', suffix='Complete', bar_length=50)
for item in items:
    # Do stuff...
    sleep(0.1)
    # Update Progress Bar
    i += 1
    print_progress(i, l, prefix='Progress:', suffix='Complete', bar_length=50)
