FROM nethacker/ubuntu-18-04-python-3:python-3.7.3

COPY requirements.txt /root
RUN pip install --upgrade pip
RUN pip install -r /root/requirements.txt

RUN useradd -m ubuntu
USER ubuntu

WORKDIR /srv/osdg
COPY osdg/ /srv/osdg/

ENV HOME=/home/ubuntu
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

EXPOSE 5000

CMD ["python3", "application.py"]
