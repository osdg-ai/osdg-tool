#!/bin/sh

echo "Updating Repositories, enabling HTTP"
#Update Repositories
sudo apt update

#Ensure that HTTP trafic is allowed through port 80
sudo ufw allow http

#Install python3 + essential libraries
echo "Installing python"
sudo apt install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

#Downloading Data files and dependencies
echo "Downloading the required data files"
python get_data.py

#Building a docker image out the data
echo "Building Docker Image"
sudo docker build -t technoteai/osdg:latest .

#Run docker image
echo "Running Docker Image"
sudo docker run --name my-osdg --detach -p 5000:5000 technoteai/osdg:latest

