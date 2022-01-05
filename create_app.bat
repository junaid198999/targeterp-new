#!/bin/bash
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
git clone https://samerda:Samer.1975@github.com/samerda/Target-Web-App.git
git clone https://samerda:Samer.1975@github.com/samerda/target-demodb.git
cd Target-Web-App
sudo docker-compose up -d
echo "__version__ = '3.1.0'" > __init__.py
sudo docker cp __init__.py $(sudo docker ps -aqf "name=TargetApp"):/usr/local/lib/python3.7/site-packages/jquery/__init__.py
sudo docker cp /home/ubuntu/target-demodb $(sudo docker ps -aqf "name=Postgres_DB"):/target-demodb
sudo docker exec -it $(sudo docker ps -aqf "name=TargetApp") bash -c "python manage.py makemigrations && python manage.py migrate"
sudo docker exec -it $(sudo docker ps -aqf "name=Postgres_DB") bash -c "pg_restore -U postgres -h localhost -v -c -d target_appdb /target-demodb/DemoDB.sql"
