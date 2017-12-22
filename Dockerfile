FROM nginx:alpine

RUN apk add --no-cache certbot openssl

WORKDIR /etc/nginx/conf.d/

ADD conf/* /etc/nginx/conf.d/
ADD renew.sh /etc/periodic/daily/
ADD entrypoint.sh certbot-domains.py certbot-certname.py /

VOLUME /etc/letsencrypt /var/lib/letsencrypt

# ENV HTTPS_DOMAINS
# ENV HTTP_DOMAINS
# ENV CERTBOT_EMAIL
# ENV CERTBOT_ARGS

CMD /entrypoint.sh
