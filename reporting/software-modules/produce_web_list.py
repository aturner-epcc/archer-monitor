#!/usr/bin/env python
#
# Produce list of software modules for website
#

from datetime import datetime, timedelta
import sys
import os

###############################################################
# Configuration section
###############################################################
indir = os.environ['ARCHER_MON_LOGDIR'] + '/modules'
outdir = os.environ['ARCHER_MON_OUTDIR'] + '/modules'

###############################################################
# End Configuration section
###############################################################

# Get the filename for yesterday's defaults
now = datetime.today()
logdate = now - timedelta(days=1)
filename = "{0}/{1}.avail".format(indir, logdate.strftime("%Y-%m-%d"))
print filename

if os.path.isfile(filename):
   datafile = open(filename, 'r')
else:
   sys.stderr.write("File does not exist: {1}".format(filename))
   sys.exit(1)

# Loop over lines in the file
moddict = {}
for line in datafile:
    if line.startswith('#'):
       continue
    line = line.rstrip()
    tokens = line.split('/')
    if len(tokens) == 1:
        print "{0:20s}".format(tokens[0])
    else:
        print "{0:20s} {1:20s}".format(tokens[0], tokens[1])

sys.exit(0)

