export EMAIL_STATUS=%EMAIL_STATUS:1%

#----------------------------------------------------------------------------------
# The task calling this should be created using the add_email_status_task method
# of a suite or family object.
# This function toggles the recipient list of the whole family of the calling
# task between 3 states:
# - none  + no emails sent, variable $EMAIL_STATUS=1
# - admin + emails sent to the admin group, variable $EMAIL_STATUS=2
# - all   + emails sent to actual recipients, bcc: admin  variable $EMAIL_STATUS=3
#----------------------------------------------------------------------------------
function toggle_email_status {
    family=$(dirname $ECF_NAME)
    states='none admin all none'
    set $states
    count=$#
    shift $EMAIL_STATUS
    newstate=$1
    EMAIL_STATUS=$((EMAIL_STATUS + 1))
    if [[ $EMAIL_STATUS -eq $count ]]; then
        EMAIL_STATUS=1
    fi
    # if the variable is not defined for that node, we need to add it
    set +e
    ecflow_client --alter $family add variable EMAIL_STATUS $EMAIL_STATUS
    set -e
    ecflow_client --alter $family change variable EMAIL_STATUS $EMAIL_STATUS
    set +e
    ecflow_client --alter $ECF_NAME change label recipients $newstate
    set -e
}

#----------------------------------------------------------------------------------
# Call this function to send an email, possibly with attachments.
# The arguments are:
# arg1: name of the product (entry name in the email template file)
# arg2: full name of the template file expected to be found in the config directory
# args: any number of extra arguments are full paths to files to attach. The
#       following formats are supported: .png .csv .txt .pdf .jpg .jpeg
# Please see documentation the template file.
#----------------------------------------------------------------------------------
function send_email {
    path=%SCHEDULER_PATH%
    python $path/emailreports.py $@
}
