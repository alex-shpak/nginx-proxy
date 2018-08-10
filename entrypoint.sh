#!/bin/sh
set -e

# Prepare nginx configuration
HTTP_DOMAINS=$(echo "$NGINX_PROXY_PASS"     | gen.py http)
HTTPS_DOMAINS=$(echo "$NGINX_PROXY_PASS"    | gen.py https)
CERBOT_DOMAINS=$(echo "$NGINX_PROXY_PASS"   | gen.py certbot)
NGINX_UPSTREAMS=$(echo "$NGINX_PROXY_PASS"  | gen.py upstreams)

export HTTP_DOMAINS
export HTTPS_DOMAINS

envsubst '$HTTP_DOMAINS $HTTPS_DOMAINS' < http.conf.tpl > http.conf
echo "$NGINX_UPSTREAMS" > upstreams.conf

# Write custom nginx config
if [[ ! -z $NGINX_CUSTOM_CONFIG ]]; then
  echo "$NGINX_CUSTOM_CONFIG" > custom.conf
fi

# Request certificates at first start (if there are any https hosts)
if [ ! -z $HTTPS_DOMAINS ] && [ ! -e /etc/letsencrypt/live ]; then
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
crond
nginx -g "daemon off;"
