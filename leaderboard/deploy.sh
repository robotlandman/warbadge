#!/bin/bash
set -e
# Give the user running the service sudo access for this command and this command only:
sudo cp /home/warbadge/warbadge/leaderboard/conf/warbadge_supervisor.conf /etc/supervisor/conf.d/
source /home/warbadge/.virtualenvs/warbadge/bin/activate
# Install new package in the venv
python setup.py install
supervisorctl --serverurl=unix:///var/run/supervisor.sock restart warbadge
