# syntax=docker/dockerfile:1

FROM python:3.9
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY m3_save_images.py m3_save_images.py

CMD [ "python3", "m3_save_images.py" ]