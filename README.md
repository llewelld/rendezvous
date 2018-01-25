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
service nginx reload.

## Continuous Authentication Service

The package installs the pico-continuous service to support continuous 
authentication. Systemd support is included for managiing the service. The
following commnds can be used.

Check status:
```
systemctl status pico-continuous.service
sudo journalctl -u pico-continous
gdbus introspect --system --dest uk.ac.cam.cl.pico.service --object-path /PicoObject
```

Start, stop, reload, enable, disable:
```
systemctl start pico-continuous.service
systemctl stop pico-continuous.service
systemctl daemon-reload
systemctl enable pico-continuous.service
systemctl disable pico-continuous.service
```

The systemd unit configuration can be found at:
```
/lib/systemd/system/pico-continuous.service
```

The dbus policy that allows the service to use the system bus can be found at:
```
/etc/dbus-1/system.d/uk.ac.cam.cl.pico.service.conf
```

## License

rendezvous is released under the AGPL licence. Read COPYING for information.

## Contributing

We welcome comments and contributions to the project. If you're interested in contributing please see here: https://get.mypico.org/cla/

Contact and Links
=================

More information can be found at: http://mypico.org

The Pico project team:
 * Frank Stajano (PI), Frank.Stajano@cl.cam.ac.uk
 * David Llewellyn-Jones, David.Llewellyn-Jones@cl.cam.ac.uk
 * Claudio Dettoni, cd611@cam.ac.uk
 * Seb Aebischer, seb.aebischer@cl.cam.ac.uk
 * Kat Krol, kat.krol@cl.cam.ac.uk
