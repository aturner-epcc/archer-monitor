#!/usr/bin/env python
#
# Plot the hostorical usage level of the machine. Depends on the
# ARCHER_MON_LOGDIR, ARCHER_MON_OUTDIR environment variables being set and on 
# PYTHONPATH including $ARCHER_MON_BASEDIR/reporting/modules
#
# Usage example:
#  plot_queues.py 1d,2d queues 
#
# First argument is list of periods to plot, second argument is
# the stem to use for the output filename
#

# Custom Python module in $ARCHER_MON_BASEDIR/reporting/modules
from timelineplot import compute_multiple_timeline, get_filelist, plot_timeline, plot_multiple_timeline

from datetime import datetime, timedelta
import sys
import os

###############################################################
# Configuration section
###############################################################
ncol = 6 # This is the number of columns of y-data in the log files

indir = os.environ['ARCHER_MON_LOGDIR'] + '/usage'
outdir = os.environ['ARCHER_MON_OUTDIR'] + '/usage'

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
    allusage = [[] for x in xrange(0,ncol)]
    for file in files:
        filename = os.path.basename(file)
        filedate = filename.split('.')[0]
        fdate = datetime.strptime(filedate, "%Y-%m-%d")
        if fdate >= startfile:
            # Read and average data from this file
            (dates, usage) = compute_multiple_timeline(ncol, intervals[curperiod], file, scale=24.0)
            alldates.extend(dates)
            for i in range(ncol):
                allusage[i].extend(usage[i])

    imgfile = "{0}/{1}_{2}.png".format(outdir, filestem, curperiod)
    titles = ["Small\n(0-96 cores)","Medium\n(97-1,536 cores)","Large\n(1,537-6,144 cores)","V. Large\n(6,145-12,288 cores)","Huge\n(12,289-118,080 cores)"]
    plot_multiple_timeline(alldates, allusage[:][1:6], startdate, now, 'Cores', titles, imgfile, stacked=True, ymax=24.0*4920)

sys.exit(0)

