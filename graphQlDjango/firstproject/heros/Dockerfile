FROM python:3.6
ENV PYTHONUNBUFFERED 1
LABEL version='1.0'
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 9000
# CMD exec gunicorn fiboschool.wsgi:application --bind 0.0.0.0:9000 --workers 3 --timeout 86400
CMD exec gunicorn heros.wsgi:application --bind 0.0.0.0:9000 --worker-class=gevent  --worker-connections=10 --workers 3 --max-requests=100 --keep-alive 300 --timeout 86400
# CMD python manage.py runserver 0.0.0.0:8000

