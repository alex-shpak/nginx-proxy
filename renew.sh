#!/bin/sh
/usr/bin/certbot renew --no-self-upgrade --webroot -w /var/lib/letsencrypt/
nginx -s reload