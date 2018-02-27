# rendezvous ReadMe

The Pico project is liberating humanity from passwords. See https://www.mypico.org

rendezvous is an implementation of the Pico Rendezvous Point. It acts as an untrusted intermediary, allowing a Pico client to communicate with a Pico server in such a way that both make outgoing HTTP/S connections to the Rendezvous Point. This way, firewalls and NATs don't cause Pico trouble.

# Installation on Nginx

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

## License

rendezvous is released under the AGPL licence. Read COPYING for information.

## Contributing

We welcome comments and contributions to the project. If you're interested in contributing please see here: https://get.mypico.org/cla/

## Contact and Links

More information can be found at: https://mypico.org

The Pico project team at time of release:
 * Frank Stajano (PI)
 * David Llewellyn-Jones
 * Claudio Dettoni
 * Seb Aebischer
 * Kat Krol

You can get in contact with us at team@cambridgeauthentication.com
