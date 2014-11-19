#!/bin/bash
#############################################################
# running_applications.bash
#############################################################
#
# Get list of currently placed applications. This
# script is desgined to be run periodically to get
# a kist of placed applications (e.g. every hour).
#
# A. R. Turner, EPCC 2014
#
#############################################################
# Configuration
#############################################################
#
# Command to list the job status
APSTAT=apstat

# Get the lines from the APSTAT command into an array
IFS=$'\r\n' apps=($($APSTAT))

# Write the start indicator and timestamp 
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`

outfile="$ARCHER_MON_LOGDIR/usage/$DATE.usage"

declare -a sizes=(4 64 256 512 4920)
declare -a usedbysize=(0 0 0 0 0)
declare -a size_labels=("Small" "Medium" "Large" "V. Large" "Huge")
nsize=${#sizes[@]}

# Test that we have some data from job list
if [ "${#apps[@]}" == 0 ]; then
   printf "%s %d\n" $TIME 0 >> $outfile
   exit 0
fi

# Initialise flag to indicate if we are in application list
inapps=0

# Loop over all lines in APSTAT output
usednodes=0
for line in "${apps[@]}"
do
   # Are we currently in the list of apps?
   if [ $inapps == 0 ]; then
      # No, look for the start of app list
      if [[ $line =~ Apid ]]; then
         inapps=1
      fi
   else
      # Yes, check for end of app list
      if [[ ! $line =~ ^[0-9] ]]; then
         inapps=0
      else 
         # Print this app line
         IFS=' ' read -a tokens <<< "${line}"
         usednodes=$(( usednodes + tokens[4] ))
         for i in {0..4}
         do
            if [ "${sizes[$i]}" -ge "$usednodes" ]; then
               usedbysize[$i]=$(( ${usedbysize[$i]} + usednodes )) 
               break
            fi
         done
      fi
   fi
done

output=`printf "%s %d" $TIME $usednodes`
echo $output ${usedbysize[@]} >> $outfile

exit 0
