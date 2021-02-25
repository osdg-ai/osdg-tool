
#Use Python as base image
FROM nethacker/ubuntu-18-04-python-3:python-3.7.3

#Copy requirements.txt into root and cd into root
COPY requirements.txt /root/
WORKDIR  /root/

#Install requirements and download spacy
RUN pip install -r /root/requirements.txt && useradd -m ubuntu
RUN python -m spacy download en_core_web_sm

#Set Environemnt and user
ENV HOME=/home/ubuntu
USER ubuntu

#Copy the files to the ubuntu user dorectory and cd into it
COPY . /home/ubuntu/
WORKDIR /home/ubuntu/

#Expose port and start app 
EXPOSE 5000

CMD ["python", "application.py"]

