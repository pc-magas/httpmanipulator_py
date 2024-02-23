#!/usr/bin/env sh

usermod -u ${APP_UID} manipulator
groupmod -g ${APP_GID} manipulator

chown -R manipulator:manipulator /opt/manipulator
chown manipulator:manipulator /var/log/manipulator

if [ ! -d "/opt/manipulator/venv" ]; then
    # Create virtual environment
    su -c "python -m venv /opt/manipulator/venv" manipulator
fi

su -c "source /opt/manipulator/venv/bin/activate" manipulator
su -c "pip install -r requirements.txt" manipulator
su -c "python /opt/manipulator/src/main.py" manipulator