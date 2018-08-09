#!/bin/sh
set -e

# Prepare nginx configuration
HTTP_DOMAINS=$(gen.py http)
HTTPS_DOMAINS=$(gen.py https)
CERBOT_DOMAINS=$(gen.py certbot)
NGINX_UPSTREAMS=$(gen.py upstreams)

export HTTP_DOMAINS
export HTTPS_DOMAINS

envsubst '$HTTP_DOMAINS $HTTPS_DOMAINS' < "http.conf.tpl" > "http.conf"
echo "$NGINX_UPSTREAMS" > upstreams.conf

if [[ ! -z $NGINX_CUSTOM_CONFIG ]]; then
  echo "$NGINX_CUSTOM_CONFIG" > custom.conf
fi

# Request certificates at first start
if [ ! -e /etc/letsencrypt/live ]; then
  certbot certonly --standalone --non-interactive $CERTBOT_ARGS \
    --cert-name cert \
    --agree-tos --email $CERTBOT_EMAIL \
    $CERBOT_DOMAINS
fi

# Generate dhparams if not existing yet
if [ ! -e /var/lib/letsencrypt/dhparam.pem ]; then
  openssl dhparam -out /var/lib/letsencrypt/dhparam.pem 2048
fi

# Start
cat http.conf
crond
nginx -g "daemon off;"
