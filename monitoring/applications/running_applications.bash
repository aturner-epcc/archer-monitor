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

# Test that we have some data from job list
if [ "${#apps[@]}" == 0 ]; then
   exit 1
fi

# Write the start indicator and timestamp 
TIME=`date --rfc-3339=seconds`
printf "__START %s\n" $TIME

# Initialise flag to indicate if we are in application list
inapps=0

# Loop over all lines in APSTAT output
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
         echo "$line"
      fi
   fi
done

# Write the end indicator
printf "__END %s\n" $TIME

exit 0
