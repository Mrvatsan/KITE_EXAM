#!/usr/bin/env bash
# exit on error
set -o errexit

if [ -d "backend" ]; then
  cd backend
fi

pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python create_superuser.py
