#!/usr/bin/env python
#
# Plot the cpu and memory usage
#
import numpy as np
import datetime
import time
from datetime import datetime
from datetime import timedelta
import sys
import os

######################################################
# Settings
######################################################
base_dir = os.environ['ARCHER_MON_BASEDIR']

# Get today's dateA
now = datetime.today()
one_day = now - timedelta(days=1)
two_days = now - timedelta(days=2)
one_week = now - timedelta(days=7)
one_month = now - timedelta(days=30)
one_quarter = now - timedelta(days=90)
one_year = now - timedelta(days=365)

logfile = sys.argv[1]
filestem = logfile.split('.')[0]

infile = open(base_dir + "/logs/" + logfile, "r")
lines = infile.read().splitlines()
infile.close()

date = []

cpu_us = []

mem_tot = []
mem_usd = []
mem_fre = []

for line in lines:
   # Skip comments
   if line.startswith('#'):
      continue
   tokens = line.split()
   timestring = tokens[0] + " " + tokens[1]
   timestring = timestring.split('+')[0]
   timetuple = datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
   date.append(timetuple)

   cpu_us.append(float(tokens[2]))

   mem = tokens[3].strip('M')
   mem_tot.append(int(mem))

   mem = tokens[4].strip('M')
   mem_usd.append(int(mem))

   mem = tokens[5].strip('M')
   mem_fre.append(int(mem))

# Plot the data
import matplotlib
matplotlib.rcParams['font.size'] = 8
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import dates

fig = plt.figure(1)

fig.subplots_adjust(right=0.8, left=0.15)

# ax1.fill_between(date, 0, cpu_us, facecolor='red', alpha='0.5', label='Load')
ax1 = plt.subplot(2, 1, 1)
ax1.set_ylim((0,80))
ax1.set_ylabel("CPU / Avg. Load")
ax1.tick_params(axis='x', labelbottom='off')

ax2 = plt.subplot(2, 1, 2)
#ax2.fill_between(date, 0, mem_tot, facecolor='blue', alpha='1.0', label='Total')
#ax2.fill_between(date, 0, mem_usd, facecolor='red', alpha='1.0', label='Used')
#ax2.fill_between(date, 0, mem_fre, facecolor='green', alpha='1.0', label='Free')
ax2.set_ylim(bottom=0)
ax2.set_ylabel("Mem / GB")


# ax2 = ax1.twinx()

# Plot 1 day
ax1.plot(date, cpu_us, 'r-', label='Load')
ax1.set_xlim((one_day,now))
ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax2.plot(date, mem_tot, "b-", label='Total')
ax2.plot(date, mem_usd, "r-", label='Used')
ax2.plot(date, mem_fre, "g-", label='Free')
ax2.set_xlim((one_day,now))
ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=120))
ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d %H:%M"))
ax2.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig.autofmt_xdate()
fig.savefig(filestem + "_1d.png")
# Plot 2 days
ax1.set_xlim((two_days,now))
ax2.set_xlim((two_days,now))
ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=240))
ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d %H:%M"))
fig.autofmt_xdate()
fig.savefig(filestem + "_2d.png")
# Plot 1 week
ax1.set_xlim((one_week,now))
ax2.set_xlim((one_week,now))
ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=720))
ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d %H:%M"))
fig.autofmt_xdate()
fig.savefig(filestem + "_1w.png")
# Plot 1 month
ax1.set_xlim((one_month,now))
ax2.set_xlim((one_month,now))
ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=2880))
ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()
fig.savefig(filestem + "_1m.png")
# Plot 1 quarter
ax1.cla()
x = np.array(cpu_us)
n = x.size
nmax = (n / 96) * 96
use = np.reshape(x[:nmax], (96,-1))
avuse = np.average(use, axis=1)
print "{0} {1} {2} {3}".format(n, nmax, len(date[::94]), avuse.size)
ax1.plot(date[::94], avuse, 'r-', label='Load')
ax1.set_xlim((one_quarter,now))
ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax2.set_xlim((one_quarter,now))
ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=8640))
ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()
fig.savefig(filestem + "_1q.png")
# Plot 1 year
ax1.set_xlim((one_year,now))
ax2.set_xlim((one_year,now))
ax2.xaxis.set_major_locator(dates.MinuteLocator(interval=34560))
ax2.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()
fig.savefig(filestem + "_1y.png")
