#!/usr/bin/env python
#
# Plot the historical usage level of the MOM nodes. Depends on the
# ARCHER_MON_LOGDIR, ARCHER_MON_OUTDIR environment variables being set and on 
# PYTHONPATH including $ARCHER_MON_BASEDIR/reporting/modules
#
# Usage example:
#  plot_mom_load.py 1d,2d mom1 
#
# First argument is list of periods to plot, second argument is
# the MOM node to plot usage for
#

# Custom Python module in $ARCHER_MON_BASEDIR/reporting/modules
from timelineplot import compute_multiple_timeline, get_filelist, plot_timeline, plot_multiple_timeline

from datetime import datetime, timedelta
import sys
import os

###############################################################
# Configuration section
###############################################################
ncol = 5 # This is the number of columns of y-data in the log files

indir = os.environ['ARCHER_MON_LOGDIR'] + '/nodes'
outdir = os.environ['ARCHER_MON_OUTDIR'] + '/nodes'

# Valid reporting periods
periods = ['1d', '2d', '1w', '1m', '1q', '1y']

# Intervals assume a 15 minute sampling interval
intervals = {
    '1d': 1,
    '2d': 2,
    '1w': 8,
    '1m': 12,
    '1q': 48,
    '1y': 48
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
files = get_filelist(indir, filestem + '.load')

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
            (dates, usage) = compute_multiple_timeline(ncol, intervals[curperiod], file)
            alldates.extend(dates)
            for i in range(ncol):
                allusage[i].extend(usage[i])

    imgfile = "{0}/{1}_{2}.png".format(outdir, filestem, curperiod)
    titles = ['Total', 'Use', 'Free', 'Cache']
    #plot_multiple_timeline(alldates, allusage[1:][:], startdate, now, 'Mem / GB', titles, imgfile, totals=False)

    import matplotlib
    matplotlib.rcParams['font.size'] = 8
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    from matplotlib import dates

    # n = len(timeline)
    fig = plt.figure(1)

    # ax1.fill_between(date, 0, cpu_us, facecolor='red', alpha='0.5', label='Load')
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_ylabel("CPU / Avg. Load")
    ax1.tick_params(axis='x', labelbottom='off')

    ax2 = plt.subplot(2, 1, 2)
    ax2.set_ylim(auto=True)
    ax2.set_ylabel("Mem / GB")

    ax1.plot(alldates, allusage[0][:], 'r-', label='CPU Load')
    ax1.set_xlim((startdate, now))
    ax1.legend()

    ax2.plot(alldates, allusage[1][:], "b-", label='Total')
    ax2.plot(alldates, allusage[2][:], "r-", label='Used')
    ax2.plot(alldates, allusage[3][:], "g-", label='Free')
    ax2.plot(alldates, allusage[4][:], "g--", label='Cache')
    ax2.set_xlim((startdate, now))
    ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d %H:%M"))
    ax2.legend()

    fig.autofmt_xdate()
    fig.savefig(imgfile)
    plt.close(fig)

sys.exit(0)

