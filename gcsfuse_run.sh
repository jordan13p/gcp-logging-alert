#!/usr/bin/env bash
# [START cloudrun_fuse_script]

# Set environment variables from file
export $(grep -v '^#' .env | xargs -d '\n' -e) &>/dev/null

# Create mount directory for service
mkdir -p $LOCAL_MNT_DIR

echo "Mounting GCS Fuse."
# --foreground --debug_gcs --debug_fuse
gcsfuse --only-dir $BUCKET_MNT_DIR $BUCKET $LOCAL_MNT_DIR
echo "Mounting completed."

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app &

# Exit immediately when one of the background processes terminate.
wait -n
# [END cloudrun_fuse_script]
