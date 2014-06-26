#!/bin/bash --login

# Get current date/time
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`

# Get the list of current default modules
defaults=`module -t avail 2>&1 | grep "(default)"`

# File name
outfile="$ARCHER_MON_BASEDIR/logs/modules/$DATE.defaults"

# Print data:
echo "# ++ $TIME" > $outfile
for line in $defaults; do
   if [[ ! $line =~ ":" ]]; then
       echo $line >> $outfile
   fi
done
