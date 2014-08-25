#
# Module with functions for plotting timelines from 
# monitoring data
#

from datetime import datetime
import numpy as np
import sys
import os.path
from glob import glob

def get_filelist(dir, ext):
    """
    Get list of date files in the specified directory
    """

    files = []
    if os.path.exists(dir):
        files = glob(os.path.join(dir, '*.' + ext))
        files.sort()
    else:
        sys.stderr.write("Directory does not exist: {1}".format(dir))
        sys.exit(1)

    return files


def compute_timeline(interval, infile):
    """
    Return dates and a timeline from specified file averaged over the 
    specified interval.
    
    Arguments
        * interval (Integer) - The interval to average over
        * infile (String) - The input file name
    """

    # Test if the file exists and open
    datafile = None
    if os.path.isfile(infile):
        datafile = open(infile, 'r')
    else:
        sys.stderr.write("File does not exist: {1}".format(infile))
        sys.exit(1)

    # Loop over lines in the file
    icount = 0
    sum = 0
    dates = []
    timeline = []
    for line in datafile:
        if line.startswith('#'):
          continue
        line = line.rstrip()
        tokens = line.split()


        icount += 1
        sum += int(tokens[2])
 
        # If at the end of the interval then compute the mean
        if icount == interval:
            # Construct a time tuple from the date
            timestring = tokens[0] + " " + tokens[1]
            timestring = timestring.split('+')[0]
            timetuple = datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")

            dates.append(timetuple)
            timeline.append(float(sum)/interval)

            icount = 0
            sum = 0

    datafile.close()

    return dates, timeline

def compute_multiple_timeline(ncol, interval, infile, scale=1.0):
    """
    Return dates and a timeline from specified file averaged over the 
    specified interval.
    
    Arguments
        * ncol (Integer) - Number of columns of y-data to read
        * interval (Integer) - The interval to average over
        * infile (String) - The input file name
    """

    # Test if the file exists and open
    data = None
    if os.path.isfile(infile):
        data = np.genfromtxt(infile, dtype=None)
    else:
        sys.stderr.write("File does not exist: {1}".format(infile))
        sys.exit(1)

    m = len(data)
    n = len(data[0])
    # n-2 to exclude the dates
    if ncol > n-2:
        sys.stderr.write("Too many columns requested, max={1}".format(n-2))
        sys.exit(1)

    # Loop over lines in the file
    icount = 0
    sum = [0] * ncol
    dates = []
    # Define an empty list of lists
    timeline = [[] for x in xrange(0,ncol)]
    for j in range(m):
        icount += 1
        
        for i in range(ncol):
            sum[i] += int(data[j][i+2])
 
        # If at the end of the interval then compute the mean
        if icount == interval:
            # Construct a time tuple from the date
            timestring = "{0} {1}".format(data[j][0], data[j][1])
            timestring = timestring.split('+')[0]
            timetuple = datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")

            dates.append(timetuple)
   
            for i in range(ncol):
                timeline[i].append(scale*float(sum[i])/interval)
                sum[i] = 0

            icount = 0

    return dates, timeline

def plot_timeline(timelabels, timeline, datemin, datemax, label, axislabel,
                  outfile, ymax=None):
    """
    Plot a timeline
    """

    import matplotlib
    matplotlib.rcParams['font.size'] = 8
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    from matplotlib import dates

    fig = plt.figure(1)
    ax = plt.subplot(1, 1, 1)
    ax.cla()
    ax.set_ylabel(axislabel)
    ax.plot(timelabels, timeline, 'r-')
    ax.fill_between(timelabels, 0, timeline, facecolor='r', alpha=0.25)
    ax.set_xlim((datemin, datemax))
    if ymax is not None:
        ax.set_ylim((0, ymax))
    else:
        ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d %H:%M"))
    fig.autofmt_xdate()
    fig.savefig(outfile)

def plot_multiple_timeline(timelabels, timeline, datemin, datemax, 
                           axislabel, titles, outfile, totals=True, ymax=None):
    """
    Plot a timeline
    """

    import matplotlib
    matplotlib.rcParams['font.size'] = 8
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    from matplotlib import dates

    n = len(timeline)

    total = []
    if totals:
        for i in range(len(timelabels)):
            sum = 0
            for j in range(n):
                sum += timeline[j][i]
            total.append(sum)

    fig = plt.figure(1)
    ax = plt.subplot(1, 1, 1)
    ax.cla()
    ax.set_ylabel(axislabel)
    for i in range(n):
        ax.plot(timelabels, timeline[:][i], label=titles[i])
    if totals:
        ax.plot(timelabels, total, linewidth=0.0)
        ax.fill_between(timelabels, 0, total, facecolor='grey', alpha=0.25)
    ax.legend()
    ax.set_xlim((datemin, datemax))
    if ymax is not None:
        ax.set_ylim((0, ymax))
    else:
        ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d %H:%M"))
    fig.autofmt_xdate()
    fig.savefig(outfile)

