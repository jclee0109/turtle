FROM python:3.9.0

RUN apt update

WORKDIR /home/ubuntu/

RUN mkdir .virtualenvs

WORKDIR /home/ubuntu/.virtualenvs/

RUN pip install virtualenv

RUN virtualenv turtle

SHELL ["/bin/bash", "-c"]

RUN source turtle/bin/activate

SHELL ["/bin/sh", "-c"]

WORKDIR /home/ubuntu/Turtle/

COPY ./ /home/ubuntu/Turtle/

RUN pip install gunicorn

RUN pip install -r /home/ubuntu/Turtle/requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && gunicorn -w 4 --env DJANGO_SETTINGS_MODULE=Turtle.settings Turtle.wsgi --bind 0.0.0.0:8000 --timeout=30"]
