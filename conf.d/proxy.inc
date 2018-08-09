# Reverse proxy configuration
location / {
    proxy_pass http://$upstream;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
    proxy_set_header Host $host:$server_port;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_connect_timeout 600;
    proxy_read_timeout 600;
    proxy_send_timeout 600;
}
