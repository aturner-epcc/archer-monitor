#!/bin/bash 

# The amount the time should exceed the long term average compile time before emailing a warning
WARN_FACTOR=10
# List of ADDRESSes to send mail to when averages exceed by WARN_FACTOR
ADDRESSEES="a.turner@epcc.ed.ac.uk"
# The top level working directory
TOPDIR=${PWD}
# The prefix for the logfile
LOGPREFIX="${TOPDIR}/log"
# The name of the file to compile
FILENAME=val.F90

# -- DO NOT CHANGE BELOW THIS POINT --


# Record the date of test (Unix epoch time)
TESTDATE=$( date +%s )
# Set up a unique test directory to run the compiles in
TESTDIR="${TOPDIR}/$$k"
mkdir -p ${TESTDIR}
cd ${TESTDIR}

# Calculate the average elapsed time of pervious runs
IFORT_AVG=$( awk 'BEGIN { count = 0; sum=0; } // {count = count+1; sum=sum+$2; } END { printf( "%.2f",sum/count) }' ${LOGPREFIX}.ifort )
CCE_AVG=$( awk 'BEGIN { count = 0; sum=0; } // {count = count+1; sum=sum+$2; } END { printf("%.2f",sum/count) }' ${LOGPREFIX}.cce )
# Work out the value of the warning.
IFORT_WARNING=$( echo ${IFORT_AVG} "*" ${WARN_FACTOR} | bc )
CCE_WARNING=$( echo ${CCE_AVG} "*" ${WARN_FACTOR} | bc )


# Write the output file to disk
FILE=${TESTDIR}/${FILENAME}
cat <<EOF > $FILE
      program keys

      use mpi
      implicit none
      !!include 'mpif.h'
      
      integer max_tag, ierr
      logical flag
 
      call MPI_Init(ierr)
      call MPI_Comm_get_attr(MPI_COMM_WORLD,MPI_TAG_UB,max_tag,flag,ierr)
      print *,'max_tag=', max_tag
 
      call MPI_Finalize(ierr)
      end program
EOF

# Compile the files and record the time taken via /usr/bin/time command
CCE_TIME=$( { /usr/bin/time -f %e bash --login -c "ftn -c val.F90 >/dev/null 2>&1"; } 2>&1 )
IFORT_TIME=$( { /usr/bin/time -f %e bash --login -c "module swap PrgEnv-cray PrgEnv-intel; /usr/bin/time -p ftn -c val.F90 >/dev/null 2>&1"; } 2>&1 )

# Log the compile test data
echo ${TESTDATE} $IFORT_TIME >> ${LOGPREFIX}.ifort
echo ${TESTDATE} $CCE_TIME >> ${LOGPREFIX}.cce

# Check to see if times exceed warning levels. If so email a warning
if [[ $( echo "${IFORT_TIME}" ">" ${IFORT_WARNING} | bc ) == "1" ]] || [[ $( echo "${CCE_TIME}" ">" ${CCE_WARNING} | bc ) == "1" ]]; then

  echo "Threshold times have been exceeded ... Sending a warning"
  for ADDRESS in ${ADDRESSEES}
  do
    echo "Emailng ${ADDRESS}"
    echo "Warning the most recent tests of compile time have found times exceeding long term averages.
The Intel compiler is recorded as taking ${IFORT_TIME}s compared to an average time of ${IFORT_AVG} seconds.
The Cray compiler is recorded as taking ${CCE_TIME}s compared to an average time of ${CCE_AVG} seconds." | mailx -s "Warning compile times exceeding averages" ${ADDRESS}
  done
fi

# Go back to the topdir and remove the test directory
cd ${TOPDIR}
rm -rf ${TESTDIR}

