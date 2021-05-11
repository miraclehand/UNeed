$sudo pip3 install gunicorn
$sudo apt-get install nginx
$sudo apt-get install rabbitmq-server
$sudo pip3 install celery
$sudo apt-get install default-jre
$sudo vi /etc/nginx/sites-available/default
$cat /etc/nginx/sites-available/default
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name UNEED;

        location / {
            proxy_pass http://125.183.209.195:8100;
        }
    }
$sudo service nginx restart

* mongodb error (=>Pymongo keeps refusing the connection at 27017)
    => hikey
        $ sudo rm /var/lib/mongodb/mongod.lock
        $ sudo service mongodb start

* mongodb error (=>Pymongo keeps refusing the connection at 27017)
    => aws
        $ sudo rm /var/lib/mongo/mongod.lock
        $ sudo service mongod start


