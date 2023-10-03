FROM python:3.11-slim

WORKDIR /src

# install system dependencies
RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# HINT: All 3x2 + Bondy
ENV SECRET_KEY foo

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY . /src