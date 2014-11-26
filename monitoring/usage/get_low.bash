#!/bin/bash
#############################################################
# get_low.bash
#############################################################
#
# Check if low priority queue is enabled or not. This
# script is desgined to be run periodically
#
# A. R. Turner, EPCC 2014
#
#
lowqueue=`qstat -q low | grep low`
enabled=`echo $lowqueue | awk '{print $10}'`
nrun=`echo $lowqueue | awk '{print $6}'`
nqueue=`echo $lowqueue | awk '{print $7}'`

# Write the start indicator and timestamp 
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`
NICEDATE=`date +"%H:%M, %A %d %B %Y"`

# Add info to log
logfile="$ARCHER_MON_LOGDIR/usage/$DATE.low"
if [ -z $enabled ]
then
   echo $TIME "S" "0" "0" >> $logfile
else
   echo $TIME $enabled $nrun $nqueue >> $logfile
fi

# Write HTML fragment for status webpage
htmlfile="$ARCHER_MON_OUTDIR/usage/low.html"
if [ $enabled == "R" ]
then
cat > $htmlfile <<EOF
<div id="machine_status_up">
   <p>Low Priority: <span style="color: green">Enabled</span></p>
   <p>Last Updated: $NICEDATE</p>
</div>
EOF
else
cat > $htmlfile <<EOF
<div id="machine_status_down">
   <p>Low Priority: <span style="color: red">Disabled</span></p>
   <p>Last Updated: $NICEDATE</p>
</div>
EOF
fi

exit 0
