#!/bin/bash
#############################################################
# get_raid.bash
#############################################################
#
# Get the current status of RAID check
#
# A. R. Turner, EPCC 2015
#
#############################################################
# Configuration
#############################################################
#
# Command to list the RAID check status
RAID_CHECK="raidStatus log"

# Get the current status
raid_status=`$RAID_CHECK`

# Write the start indicator and timestamp 
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`
NICEDATE=`date +"%H:%M, %A %d %B %Y"`

outfile="$ARCHER_MON_LOGDIR/raid/$DATE.raid"

echo $TIME $raid_status >> $outfile

# Write HTML fragment for status webpage
fslist="fs2 fs3 fs4"
htmlfile="$ARCHER_MON_OUTDIR/usage/raid.html"
echo "" > $htmlfile
for fs in $fslist; do
   raid_stat=`raidStatus $fs`
   if [ $raid_stat == "1" ]; then
cat >> $htmlfile <<EOF
<div id="machine_status_up">
   <p>RAID Check, ${fs}: <span style="color: green">Running</span></p>
   <p>Last Updated: $NICEDATE</p>
</div><br />
EOF
else
cat >> $htmlfile <<EOF
<div id="machine_status_down">
   <p>RAID Check, ${fs}: <span style="color: red">Not Running</span></p>
   <p>Last Updated: $NICEDATE</p>
</div><br />
EOF
fi
done

exit 0
