FROM ubuntu:18.04
FROM python:3.9


COPY requirements.txt /root
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /root/requirements.txt

RUN useradd -m ubuntu
USER ubuntu

WORKDIR /srv/osdg
COPY osdg/ /srv/osdg/

ENV HOME=/home/ubuntu
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

EXPOSE 5000

CMD ["python3", "application.py"]
