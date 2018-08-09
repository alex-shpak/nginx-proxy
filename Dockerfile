FROM nginx:alpine

RUN apk add --no-cache certbot openssl

WORKDIR /etc/nginx/conf.d/

ADD conf.d/* /etc/nginx/conf.d/
ADD renew.sh /etc/periodic/daily/renew
ADD entrypoint.sh gen.py /usr/bin/

VOLUME /etc/letsencrypt /var/lib/letsencrypt

CMD entrypoint.sh
