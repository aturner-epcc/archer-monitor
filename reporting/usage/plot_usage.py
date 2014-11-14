#!/usr/bin/env python
#
# Plot the hostorical usage level of the machine. Depends on the
# ARCHER_MON_LOGDIR, ARCHER_MON_OUTDIR environment variables being set and on 
# PYTHONPATH including $ARCHER_MON_BASEDIR/reporting/modules
#
# Usage example:
#  plot_usage.py 1d,2d usage 
#
# First argument is list of periods to plot, second argument is
# the stem to use for the output filename
#

# Custom Python module in $ARCHER_MON_BASEDIR/reporting/modules
from timelineplot import compute_timeline, get_filelist, plot_timeline

from datetime import datetime, timedelta
import sys
import os

###############################################################
# Configuration section
###############################################################
indir = os.environ['ARCHER_MON_LOGDIR'] + '/usage'
outdir = os.environ['ARCHER_MON_OUTDIR'] + '/usage'

# Maximum number of nodes on the system
maxnodes = 4920

# Valid reporting periods
periods = ['1d', '2d', '1w', '1m', '1q', '1y']

# Intervals assume a 15 minute sampling interval
intervals = {
    '1d': 1,
    '2d': 2,
    '1w': 8,
    '1m': 12,
    '1q': 48,
    '1y': 96
            }
days = {
    '1d': 1,
    '2d': 2,
    '1w': 7,
    '1m': 30,
    '1q': 90,
    '1y': 365
            }
###############################################################
# End Configuration section
###############################################################

speriod = sys.argv[1]
filestem = sys.argv[2]
tokens = speriod.split(',')
repperiod = []
# Make sure we have specified valid periods
for token in tokens:
    if token in periods:
        repperiod.append(token)
    else:
        print "Period {0} not found, skipping".format(token)

if len(repperiod) < 1:
    print "No valid periods specified, exiting"
    sys.exit(1)

# List of log files
files = get_filelist(indir, 'usage')

now = datetime.today()
for curperiod in repperiod:
    # We have to add one to the days to make sure we get the data
    # from the previos day that we need
    startfile = now - timedelta(days=days[curperiod]+1)
    startdate = now - timedelta(days=days[curperiod])

    alldates = []
    allusage = []
    for file in files:
        filename = os.path.basename(file)
        filedate = filename.split('.')[0]
        fdate = datetime.strptime(filedate, "%Y-%m-%d")
        if fdate >= startfile:
            # Read and average data from this file
            (dates, usage) = compute_timeline(intervals[curperiod], file)
            alldates.extend(dates)
            allusage.extend(usage)

    imgfile = "{0}/{1}_{2}.png".format(outdir, filestem, curperiod)
    plot_timeline(alldates, allusage, startdate, now, 'Usage', 'Nodes',
                  imgfile, ymax=maxnodes)

sys.exit(0)

