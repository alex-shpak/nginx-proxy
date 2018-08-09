# Global settings
server_tokens off;
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";

# http -> https redirect
server {
  listen 80;
  server_name $HTTPS_DOMAINS;

  include conf.d/certbot.inc;
  location / {
    return 301 https://$host$request_uri;
  }
}

# http hosts
server {
  listen 80;
  server_name $HTTP_DOMAINS;
  
  include conf.d/certbot.inc;
  include conf.d/proxy.inc;
}

# https hosts
server {
  listen 443 ssl default deferred;
  server_name $HTTPS_DOMAINS;

  include conf.d/ssl.inc;
  include conf.d/proxy.inc;
}
