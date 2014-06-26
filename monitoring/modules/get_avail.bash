#!/bin/bash --login

# Get current date/time
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`

# Get the list of available modules
list=`module -t avail 2>&1`

# File name
outfile="$ARCHER_MON_BASEDIR/logs/modules/$DATE.avail"

# Print data:
echo "# ++ $TIME" > $outfile
for line in $list; do
   if [[ ! $line =~ ":" ]]; then
       echo $line >> $outfile
   fi
done
