# Ssl configuration

ssl_certificate /etc/letsencrypt/live/cert/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/cert/privkey.pem;

# enable session resumption to improve https performance
# http://vincent.bernat.im/en/blog/2011-ssl-session-reuse-rfc5077.html
ssl_session_cache shared:SSL:50m;
ssl_session_timeout 5m;

# Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
ssl_dhparam /var/lib/letsencrypt/dhparam.pem;

ssl_prefer_server_ciphers on;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_ciphers "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES256-GCM-SHA384:AES128-GCM-SHA256:AES256-SHA256:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4";

# enable ocsp stapling (mechanism by which a site can convey certificate revocation information to visitors in a privacy-preserving, scalable manner)
# http://blog.mozilla.org/security/2013/07/29/ocsp-stapling-in-firefox/
# resolver 8.8.8.8;
# ssl_stapling on;
# ssl_trusted_certificate /etc/nginx/ssl/star_forgott_com.crt;

# includeSubdomains;  # disabled for now
add_header Strict-Transport-Security "max-age=31536000;";
