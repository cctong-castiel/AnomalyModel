FROM python:3.8.2

WORKDIR /app

ADD . /app

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install -r requirements.txt

EXPOSE 8964

CMD gunicorn -c ./gunicorn.conf main:app
