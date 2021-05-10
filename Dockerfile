FROM ubuntu:latest

WORKDIR /project_2-app

COPY requirements.txt .

RUN set -xe \
    && apt-get update -y\
    && apt-get install -y python3-pip
RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .