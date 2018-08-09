#!/usr/bin/python
import os, sys, argparse, re, logging
from urlparse import urlparse

PROXY_PASS_VAR = 'NGINX_PROXY_PASS'
PROXY_PASS_SEPARATOR = '->'

logging.basicConfig()
logger = logging.getLogger('gen')


def yield_upstreams():
  if not os.environ.has_key(PROXY_PASS_VAR):
    logger.warning('Proxy hosts are not defined')
    return

  for line in os.environ[PROXY_PASS_VAR].splitlines():
    pair = line.split(PROXY_PASS_SEPARATOR)

    if len(pair) != 2:
      logger.error('Wrong $%s format', PROXY_PASS_VAR)
      sys.exit(1)

    host, upstream = map(lambda it: urlparse(it.strip()), pair)

    if host.scheme not in ['http', 'https']:
      logger.error('Scheme not defined in %s, should be http or https', host.geturl())
      sys.exit(1)

    upstream.name = re.sub('[:.]', '_', upstream.netloc)
    yield (host, upstream)


def print_upstreams_file(upstreams):
  for host, upstream in upstreams:
    print 'upstream %s { server %s; }' % (upstream.name, upstream.netloc)

  print 'map $host $upstream {'
  for host, upstream in upstreams:
    print '    %s "%s";' % (host.hostname, upstream.name)
  print '}'


def print_domains(upstreams, scheme, prefix=''):
  http_domains = []
  for host, upstream in upstreams:
    if host.scheme == scheme:
      http_domains.append(host.hostname)

  print ' '.join(
    [prefix + host for host in http_domains]
  )


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('action', choices=['upstreams', 'http', 'https', 'certbot'])
  args = parser.parse_args()

  upstreams = yield_upstreams()
  if args.action == 'upstreams':
    print_upstreams_file(upstreams)

  elif args.action == 'http':
    print_domains(upstreams, 'http')

  elif args.action == 'https':
    print_domains(upstreams, 'https')

  elif args.action == 'certbot':
    print_domains(upstreams, 'https', '-d ')
