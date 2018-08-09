#!/bin/sh

# Prepare nginx configuration
HTTP_DOMAINS=`gen.py https`
HTTPS_DOMAINS=`gen.py https`
CERBOT_DOMAINS=`gen.py certbot`

cat <<EOL > variables.conf
server {
  set \$http_domains "$HTTP_DOMAINS";
  set \$https_domains "$HTTPS_DOMAINS";
}
EOL

gen.py upstreams > upstreams.conf

# Request certificates at first start
if [ ! -e /etc/letsencrypt/live ]; then
  certbot certonly --standalone --non-interactive $CERTBOT_ARGS \
    --cert-name cert \
    --agree-tos --email $CERTBOT_EMAIL \
    $CERBOT_DOMAINS # || exit $?
fi

# Generate dhparams if not existing yet
if [ ! -e /var/lib/letsencrypt/dhparam.pem ]; then
  openssl dhparam -out /var/lib/letsencrypt/dhparam.pem 2048
fi

# Start
crond
nginx -g "daemon off;"
