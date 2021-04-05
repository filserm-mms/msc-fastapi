#! /bin/bash
apt-get update
apt-get install python3-pip

sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
        software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update 

apt-get install -y docker-ce docker-ce-cli containerd.io

#useradd -m -g sudo -p  $(openssl passwd -crypt $PASSWORD) $USER

groupadd docker
#usermod -aG docker $USER

#build fastapi app
#docker build -t nginx-unit-fastapi .
#docker run -p 80:80 nginx-unit-fastapi