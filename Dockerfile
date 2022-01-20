FROM python:3.8

RUN useradd -ms /bin/bash notroot
WORKDIR /home/notroot
USER notroot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src src
COPY main.py main.py
COPY ./assets assets

