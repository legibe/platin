# wait for background process to stop.
# If we did not have background jobs, closly called foreround jobs
# may arrive out of order at the server, causing unnecessary zombies
# The wait should prevent this.

wait         # wait for background process to stop
ecflow_client --complete  # Notify ECF of a normal end
cd
rm -fr $TMPDIR/ecflow.$$
trap 0       # Remove all traps
date         # mark the end of the job
exit 0       # End the shell
