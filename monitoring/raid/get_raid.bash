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

outfile="$ARCHER_MON_LOGDIR/raid/$DATE.raid"

echo $TIME $raid_status >> $outfile

exit 0
