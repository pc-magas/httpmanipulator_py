#!/usr/bin/env sh

usermod -u ${APP_UID} manipulator
groupmod -g ${APP_GID} manipulator

chown manipulator:manipulator /var/log/manipulator

if [ ! -d "/home/manipulator/venv" ]; then
    # Create virtual environment
    echo "Create virtualenv"
    su -c "python -m venv /home/manipulator/venv" manipulator
fi

su manipulator -c "source /home/manipulator/venv/bin/activate && pip install -r requirements.txt &&  python src/main.py"