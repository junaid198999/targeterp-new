#!/bin/bash

HOSTED_ZONE_ID=16552
RESOURCE_VALUE=194.163.146.132
DNS_NAME=targeterp.targetsapps.com
RECORD_TYPE=CNAME
TTL=86400

JSON_FILE=`mktemp`

(
cat <<EOF
{
    "Comment": "Create single record set",
    "Changes": [
        {
            "Action": "CREATE",
            "ResourceRecordSet": {
                "Name": "$DNS_NAME",
                "Type": "$RECORD_TYPE",
                "TTL": $TTL,
                "ResourceRecords": [
                    {
                        "Value": "$RESOURCE_VALUE"
                    }
                ]
            }
        }
    ]
}
EOF
) > $JSON_FILE


echo "server {
    listen 80;
    server_name targeterp.targetsapps.com;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ubuntu/uwsgi/Target-Target-ERP.sock;
    }
    location /static/ {
        autoindex on;
        alias /home/ubuntu/Target-ERP/TARGET/static/;
    }
    location /media/ {
        autoindex on;
        alias /home/ubuntu/Target-ERP/TARGET/media/;
    }
}" > /etc/nginx/sites-enabled/Target-ERP


echo "[uwsgi]
home = /home/ubuntu/Target-ERP/env
chdir = /home/ubuntu/Target-ERP/
wsgi-file = /home/ubuntu/Target-ERP/config/wsgi.py

socket = /home/ubuntu/uwsgi/Target-Newtargetapp.sock
vacuum = true
chown-socket = ubuntu:www-data
chmod-socket = 660" > /home/ubuntu/uwsgi/sites/target-app-Target-ERP.ini


sudo nginx -s reload
