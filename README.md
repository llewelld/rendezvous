# Pico Rendezvous Point installation on Nginx

Note that many of these commands will need sudo.

Clone the rendezvous files into a folder nginx can access. Something like:
```
git clone cl-pico@git.csx.cam.ac.uk/i/cl-pico/pico/rendezvous.git /var/www/rendezvous
```

Ensure python and pip are installed.
```
apt-get install python python-pip virtualenv
apt-get install build-essential python-dev
```

Move into your rendezvous folder and setup the virtual environment for python.
```
cd /var/www/rendezvous
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Start the server on port 8082 (it can be any port, but this matches rendezvous.conf)
```
python v2.py -p 8082
```

To leave the virtual environment
```
deactivate
```

Add the server certificates for TLS
```
cp mypico.crt /etc/ssl/certs/
cp mypico.pem /etc/ssl/private/
```

Setup Nginx to point to the server by installing the nginx.conf as rendezvous.conf in
sites-available, making a symlink to it in sites-enabled and then editing it as
required.
```
cp /var/www/rendezvous/rendezvous.conf /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/rendezvous.conf /etc/nginx/sites-enabled/rendezvous.conf
```

Reload the nginx config
```
service nginx reload
```

