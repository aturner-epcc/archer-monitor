#!/bin/bash

# Get current time, date and host
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`
HOST=`hostname`

outfile="$ARCHER_MON_LOGDIR/nodes/${DATE}.${HOST}.load"

# Get the appropriate lines from uptime
uplines=`uptime`
# Split the lines into an array for processing
uptokens=($uplines)

# Get the appropriate lines from free
freelines=`free -g | awk '(NR>1)&&(NR<4)'`
# Split the lines into an array for processing
freetokens=($freelines)

# Print data:
#          CPU                                             Memory
#          User         System       Idle                  Total            Used             Free       Cache
echo $TIME ${uptokens[11]} ${freetokens[1]} ${freetokens[9]} ${freetokens[10]} ${freetokens[6]} >> $outfile
