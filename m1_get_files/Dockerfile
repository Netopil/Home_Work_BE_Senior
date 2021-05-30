# syntax=docker/dockerfile:1

FROM python:3.9
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

COPY m1_get_files.py m1_get_files.py

CMD [ "python3", "m1_get_files.py" ]