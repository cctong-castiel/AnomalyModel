FROM python:3.8.2

WORKDIR /app

ADD . /app

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install gunicorn
RUN python3 -m pip install toolz
RUN python3 -m pip install fsspec>=0.3.3
RUN python3 -m pip install -r requirements.txt

EXPOSE 721

CMD gunicorn -c ./gunicorn.conf main:app
