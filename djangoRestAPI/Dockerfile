# FROM python:3.6
# ENV PYTHONUNBUFFERED 1
# LABEL version='1.0'
# ADD . /usr/src/app
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE 9100
# # CMD exec gunicorn fiboschool.wsgi:application --bind 0.0.0.0:9000 --workers 3 --timeout 86400
# CMD exec gunicorn kryptonite.wsgi:application --bind 0.0.0.0:9100 --worker-class=gevent  --worker-connections=10 --workers 3 --max-requests=100 --keep-alive 300 --timeout 86400
# # CMD python manage.py runserver 0.0.0.0:8000

# Pull the base image
FROM python:3.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
#Upgrade pip
RUN pip install pip -U
ADD requirements.txt /code/
#Install dependencies
RUN pip install -r requirements.txt
ADD . /code/

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev  -y