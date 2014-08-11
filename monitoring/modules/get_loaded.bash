#!/bin/bash --login

# Get current date/time
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`

# Get the list of current default modules
list=`module -t list 2>&1 | grep -v Currently`

# File name
outfile="$ARCHER_MON_LOGDIR/modules/$DATE.list"

# Print data:
echo "# ++ $TIME" > $outfile
for line in $list; do
   if [[ ! $line =~ ":" ]]; then
       echo $line >> $outfile
   fi
done
