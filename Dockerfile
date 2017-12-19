FROM nginx:alpine

RUN apk add --no-cache certbot openssl

WORKDIR /etc/nginx/conf.d/

ADD *.conf *.inc /etc/nginx/conf.d/
ADD renew /etc/periodic/daily/
ADD entrypoint.sh /
ADD certbot-domains.py /

VOLUME /etc/letsencrypt /var/lib/letsencrypt

# ENV HTTPS_DOMAINS
# ENV HTTP_DOMAINS
# ENV CERTBOT_EMAIL
# ENV CERTBOT_ARGS

CMD /entrypoint.sh
