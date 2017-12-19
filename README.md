## Nginx proxy in docker
Simple nginx reverse proxy including letsencrypt certificates auto issue and update

### Features
 - Supports multiple hosts
 - Proxying both http and https endpoints
 - Automated issue and renew for [letsencrypt](https://letsencrypt.org) certificates


### Usage
See docker compose example [docker-compose.yml](docker-compose.yml)
```yml
version: '3'
services:
  nginx:
    image: lxshpk/nginx-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      HTTPS_DOMAINS: |
        example.com
        sub1.example.com
      HTTP_DOMAINS: |
        sub2.example.com
      CERTBOT_EMAIL: mail@example.com
      CERTBOT_ARGS: --dry-run
    volumes:
      - "/var/lib/letsencrypt:/var/lib/letsencrypt"
      - "/etc/letsencrypt:/etc/letsencrypt"
      - "./upstreams.conf:/etc/nginx/conf.d/upstreams.conf"
  service:
    image: ...
    ports:
      - "8080:8080"
```

When started docker container will request SSL certificates for `example.com` and `sub.example.com` or will fail to start if not successful. Domain `sub2.example.com` will be hosted with http.


### Upstreams configurations
```conf
upstream example {
  server service:8080;
}

upstream sub1 {
  server 192.168.122.2:8080;
}

upstream sub2 {
  server 192.168.122.3:8080;
}

map $host $upstream {
  default "example";

  example.com "example";
  sub1.example.com "sub1";
  sub2.example.com "sub2";
}
```


### Variables
| Variable          | Description                           |
| --                | --                                    |
| `HTTPS_DOMAINS`   | Domains that require SSL certificates and will be redirected to `https://` |
| `HTTP_DOMAINS`    | Domains to serve with `http://`    |
| `CERTBOT_EMAIL`   | Email for registration. Note that certbot is runned with `--agree-tos` flag |
| `CERTBOT_ARGS`    | Additional flags for certbot          |
