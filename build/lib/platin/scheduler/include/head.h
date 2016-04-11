#!/bin/bash

set -x # echo script lines as they are executed
set -e # stop the shell on first error
set -u # fail when using an undefined variable

date    # mark the start of the job

# Defines the three variables that are needed for any
# communication with ECF_

export ECF_PORT=%ECF_PORT%    # ECF_ Remote Procedure Call number
export ECF_NODE=%ECF_NODE%    # The name sms that issued this task
export ECF_NAME=%ECF_NAME%    # The name of this current task
export ECF_PASS=%ECF_PASS%    # A unique password
export ECF_TRYNO=%ECF_TRYNO%  # Current try number of the task
export ECF_FILES=%ECF_FILES%
export ECF_JOBOUT=%ECF_JOBOUT%
export SUITE=%SUITE%

# Tell ECF_ we have started
# The ECF_ variable ECF_RID will be set to parameter of smsinit
# Here we give the current PID.

ecflow_client --init=$$

#----------------------------------------------------------------------------------
# Receives 2 arguments:
# - subject of the email
# - body of the email
# 
# and sends an emails to the admin(s)
# any extra argument is considered the path to a file to attach. Supported types
# are ascii files.
#----------------------------------------------------------------------------------
function send_admin_email {
    path=%SCHEDULER_PATH%
    export SCHEDULER_EMAIL=%SCHEDULER_EMAIL%
    export SCHEDULER_ADMIN=%SCHEDULER_ADMIN%
    python $path/emailadmin.py "$1" "$2"
}

# Defined a error hanlder
ERROR() {
   # wait for background process to stop.
   # If we did not have background jobs, closly called foreround jobs
   # may arrive out of order at the server, causing unnecessary zombies
   # The wait should prevent this.

	set +e         # Clear -e flag, so we don't fail
	wait           # wait for background process to stop

    # notify admins by email
    subject="Suite: $SUITE - Task $TASK failed - $ECF_NAME"
    body=$(tail -25 $ECF_JOBOUT)
    send_admin_email "$subject" "$body"

    ecflow_client --abort      # Notify ECF_ that something went wrong
	trap 0         # Remove the trap
    cd
    # when failing we don't delete the tmpdir we rename it
    # to error.pid. These are cleaned up at restart time
    mv $TMPDIR $TMPDIR_ROOT/error.$$
	exit 0         # End the script
}

# Trap any calls to exit and errors caught by the -e flag
trap ERROR 0
# Trap any signal that may cause the script to fail
trap '{ echo "Killed by a signal"; ERROR ; }' 1 2 3 4 5 6 7 8 10 12 13 15

export ECF_BIN=%ECF_BIN%
PATH=$ECF_BIN:$PATH

now=$(date '+%%Y-%%m-%%d')
export YMD=%YMD:$now%
export TRYNO=%ECF_TRYNO%
export FAMILY1=%FAMILY1:%
export TASK=%TASK%

export DELTA=%DELTA:0%
export YYYYMMDD=$(scdate $YMD $DELTA)
export TODAY=%DAY%

export CONFIG_DIR=%CONFIG_DIR%

export TMPDIR=%TMPDIR:$TMPDIR%
export TMPDIR_ROOT=$TMPDIR
mkdir -p $TMPDIR || true
export DATA_STORE=%DATA_STORE:.%
export PYTHON_EXEC=%PYTHON_EXEC:false%
export PYTHON=findpy
export PYTHON_SCRIPTS=%PYTHON_SCRIPTS:.%

export TMPDIR=$TMPDIR_ROOT/ecflow.$$
mkdir -p $TMPDIR || true
cd $TMPDIR

# now we manage whether the task should run of not, this depends on two variables
# DAY_OF_MONTH and DAY_OF_WEEK. We want to do an OR between them so that we can
# do:
# DAY_OF_WEEK=wednesday
# DAY_OF_MONTH=15
# the taks runs every wednesday and the 15th of the month.

weekly=1
has_weekly=0
# default every day of the week
export DAY_OF_WEEK="%DAY_OF_WEEK:none%"
if [[ $DAY_OF_WEEK != none ]]; then
    has_weekly=1
    days=$(echo $DAY_OF_WEEK | sed 's/,/ /g')
    dow=$(day_of_week $YYYYMMDD)
    today=0
    for day in $days; do
        if [[ $day = $dow ]]; then
            today=1
        fi
    done
    if [[ $today -ne 1 ]]; then
        weekly=0 
    fi
fi

monthly=1
has_monthly=0
# default every day of the month
export DAY_OF_MONTH="%DAY_OF_MONTH:none%"
if [[ $DAY_OF_MONTH != none ]]; then
    has_monthly=1
    days=$(echo $DAY_OF_MONTH | sed 's/,/ /g')
    dom=$(day_of_month $YYYYMMDD)
    today=0
    for day in $days; do
        if [[ $day = $dom ]]; then
            today=1
        fi
    done
    if [[ $today -ne 1 ]]; then
        monthly=0
    fi
fi

run=1
if [[ ($has_weekly -eq 1 && $weekly -eq 0) || ($has_monthly -eq 1 && $monthly -eq 0) ]]; then
    run=0
fi
if [[ $has_monthly -eq 1 && $monthly -eq 1 ]]; then
    run=1
fi
if [[ $has_weekly -eq 1 && $weekly -eq 1 ]]; then
    run=1
fi
# if it shouldn't run then include the tail so signal an successful
# end of job
if [[ $run -eq 0 ]]; then
%include% <tail.h>
fi

# if we get here then the task actually runs
