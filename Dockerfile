# Use a newer Python version with a supported Debian version
FROM python:3.10.8-slim-bullseye

# Or even better, use the latest Python 3.10 with latest Debian
FROM python:3.10-slim

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /VJ-FILTER-BOT
WORKDIR /VJ-FILTER-BOT
COPY . /VJ-FILTER-BOT
CMD ["python", "bot.py"]