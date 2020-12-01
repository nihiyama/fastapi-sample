#!/bin/sh

# connect db
PYTHONPATH=. python app/pre_start.py

# db migrate
PYTHONPATH=. alembic upgrade head

# create superuser
PYTHONPATH=. python app/create_superuser.py

# start app
if [ $APP_ENV = "development" ]; then
    PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --reload
elif [ $APP_ENV = "development" ]; then
    PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0
else
    echo "Choose development or production"
fi
