#! /bin/bash

apt-get update -y
apt-get install -y python3-pip 

apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get update 
apt install -y docker-ce


###create daemon.json --> this is needed as otherwise the routing to interconnect is not working any more
touch  /etc/docker/daemon.json 
cat <<EOT >> /etc/docker/daemon.json 
{
   "bip": "10.15.0.1/24",
   "default-address-pools": [
     {"base": "10.20.0.0/16", "size": 24},
     {"base": "10.40.0.0/16", "size": 24}
   ]
 }
EOT

systemctl restart docker

useradd -m -g sudo -p  $(openssl passwd -crypt $PASSWORD) fastapi
usermod -aG docker fastapi

###install github cli
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

###manual doing after github repo was cloned 
###build fastapi app
#docker build -t nginx-unit-fastapi .
#docker create -p 80:80 --add-host dwhflash:172.17.133.32 --name fastapi nginx-unit-fastapi
#docker start fastapi