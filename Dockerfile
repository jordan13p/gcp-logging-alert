# Python base images can't use alpine to build.
FROM python:3.10-slim

WORKDIR /app
COPY . ./

# Install system dependencies
# Install production dependencies in target folder.
RUN set -e; \
    apt-get update -y && apt-get install -y \
    curl \
    tini \
    gnupg2 \
    lsb-release; \
    gcsFuseRepo=gcsfuse-`lsb_release -c -s`; \
    echo "deb http://packages.cloud.google.com/apt $gcsFuseRepo main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list; \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key add -; \
    apt-get update; \
    apt-get install -y gcsfuse \
    && apt-get clean \
    && pip install --no-cache-dir --target=/app/dependencies -r requirements.txt \
    && chmod +x /app/gcsfuse_run.sh

# Update PATH environment variable
# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONPATH="${PYTHONPATH}:/app/dependencies" \
    PATH="$PATH:/app/dependencies/bin" \
    PYTHONUNBUFFERED=True

# Use tini to manage zombie processes and signal forwarding
# https://github.com/krallin/tini
ENTRYPOINT ["/usr/bin/tini", "--"] 

# Pass the startup script as arguments to Tini
CMD ["/app/gcsfuse_run.sh"]
