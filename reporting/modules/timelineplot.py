#
# Module with functions for plotting timelines from 
# monitoring data
#

from datetime import datetime
import sys
import os.path

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
