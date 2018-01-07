import os

# Converts HTTPS_DOMAINS env variable into list of domain params for certbot
domains = os.environ['HTTPS_DOMAINS'].split()
print ' '.join(
  ['-d %s' % domain for domain in domains]
)
