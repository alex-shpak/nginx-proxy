# certbot webroot auth
location ~ .well-known/acme-challenge/ {
  root /var/lib/letsencrypt;
  default_type text/plain;
}
