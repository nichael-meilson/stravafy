FROM python:3.11-slim

WORKDIR /src

# install system dependencies
RUN apt-get update && apt-get install -y chromium-driver

# Set environment variable to run Chrome in headless mode
ENV CHROME_DRIVER_BINARY=/usr/bin/chromium-browser
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV SECRET_KEY foo

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY . /src