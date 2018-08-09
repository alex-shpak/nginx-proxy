## Nginx proxy in docker
[![Docker Build Status](https://img.shields.io/docker/build/lxshpk/nginx-proxy.svg)](https://hub.docker.com/r/lxshpk/nginx-proxy/)  

Simple nginx reverse proxy including letsencrypt certificates auto issue and update

### Features
 - Supports multiple hosts
 - Proxying both http and https endpoints
 - Minimal configuration with env variables
 - Automated issue and renew for [letsencrypt](https://letsencrypt.org) certificates


### Usage
See docker compose example [docker-compose.yml](docker-compose.yml)

```yml
version: '3'
services:
  nginx:
    # image: lxshpk/nginx-proxy
    build: .
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    links:
      - service
    environment:
      UPSTREAMS: |
        https://example.com -> http://service:8080
        https://sub.example.com -> http://service:8081
        http://external.example.com -> http://external.com

      CERTBOT_EMAIL: mail@example.com
      CERTBOT_ARGS: --dry-run

    # volumes:
    #   - "/var/lib/letsencrypt:/var/lib/letsencrypt"
    #   - "/etc/letsencrypt:/etc/letsencrypt"

  service:
  image: ...
  ports:
    - "8080:8080"
```

When started docker container will request SSL certificates for `example.com` and `sub.example.com` or will fail to start if not successful. Domain `external.example.com` will be hosted with http.
