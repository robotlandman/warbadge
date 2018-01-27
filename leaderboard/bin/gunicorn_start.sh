#!/bin/bash
export WARBADGE_SETTINGS=/home/warbadge/warbadge_prod_config.ini 
NAME="warbadge_app"
DIR="/home/warbadge"
RUN_DIR="/home/warbadge/run"
SOCKET="${RUN_DIR}/warbadge_gunicorn.sock"
USER="warbadge"
GROUP="warbadge"
NUM_WORKERS=4
CONFIG="/home/warbadge/warbradge_prod_config.ini"
mkdir -p ${RUN_DIR}
echo "STARTING GUNICORN AS $(whoami)"

cd ${DIR}
source .virtualenvs/warbadge/bin/activate
# The app should already be installed in the venv via "setup.py install"

# Start gunicorn. We set logging to stdout so it can be handled by
# supervisord.
exec .virtualenvs/warbadge/bin/gunicorn ${NAME}  \
--workers 4 \
--user=${USER} \
--group=${GROUP} \
--bind=unix:${SOCKET} \
--log-level=debug \
--log-file=-
