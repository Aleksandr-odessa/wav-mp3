FROM python:3.10-slim

WORKDIR /server/

COPY . /server/

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get install -y ffmpeg
ADD main.py /server/

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000