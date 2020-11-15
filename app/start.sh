#!/bin/sh

# connect db
python app/pre_start.py

# db migrate
alembic upgrade head

# create superuser
python app/create_superuser.py

# start app
cd app
if [ $APP_ENV = "development" ]; then
    uvicorn main:app --reload
elif [ $APP_ENV = "development" ]; then
    uvicorn main:app
else
    echo "Choose development or production"
fi
