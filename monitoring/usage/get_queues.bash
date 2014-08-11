#!/bin/bash --login
#############################################################
# get_queues.bash
#############################################################
#
# Get load on the current queues. This
# script is desgined to be run periodically to get
# a kist of placed applications (e.g. every hour).
#
# A. R. Turner, EPCC 2014
#
# Get the lines from the QSTAT command into an array
IFS=$'\r\n' joblist=($(qstat -a))

# Write the start indicator and timestamp 
TIME=`date --rfc-3339=seconds`
DATE=`date --rfc-3339=date`

outfile="$ARCHER_MON_LOGDIR/queues/$DATE.standard"

# Test that we have some data from job list
if [ "${#joblist[@]}" == 0 ]; then
   printf "%s %d %d %d\n" $TIME 0 0 0 >> $outfile
   exit 0
fi

# Initialise flag to indicate if we are in job list
injobs=0

cpumr=0
cpumq=0
cpumh=0
for line in "${joblist[@]}"
do
   # Are we currently in the list of jobs?
   if [ $injobs == 0 ]; then
      # No, look for the start of jobs list
      if [[ $line =~ ^---- ]]; then
         injobs=1
      fi
   else
      # Yes, check for end of job list
      if [[ ! $line =~ ^[0-9] ]]; then
         injobs=0
      else 
         IFS=' ' read -a tokens <<< "${line}"
         nodes=${tokens[5]}
         walltime=${tokens[8]}
         jobstatus=${tokens[9]}
         IFS=':' read -a tokens <<< "${walltime}"
         # Strip leading zeroes
         hours=$(echo ${tokens[0]} | sed 's/0*//')
         minutes=$(echo ${tokens[1]} | sed 's/0*//')
         # Keeping in minutes to allow integer arithmetic
         totminutes=$(( hours * 60 + minutes ))
         nodemins=$(( nodes * totminutes ))
         if [[ $jobstatus == "R" ]]; then
             (( cpumr += nodemins ))
         elif [[ $jobstatus == "Q" ]]; then
             (( cpumq += nodemins ))
         elif [[ $jobstatus == "H" ]]; then
             (( cpumh += nodemins ))
         fi
      fi
   fi
done

printf "%s %d %d %d\n" $TIME $cpumr $cpumq $cpumh  >> $outfile

exit 0
