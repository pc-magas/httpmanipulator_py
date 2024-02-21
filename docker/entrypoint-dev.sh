#!/usr/bin/env sh

usermod -u ${APP_UID} manipulator
groupmod -g ${APP_GID} manipulator

chown -R manipulator:manipulator /opt/manipulator
chown manipulator:manipulator /var/log/manipulator

su -c "python /opt/manipulator/src/main.py" manipulator