import os, sys, argparse, re, logging, hashlib
from urlparse import urlparse

PROXY_PASS_LINE_PATTERN = r'^\s*(\S+)\s*->\s*(\S+)\s*$'

logging.basicConfig()
logger = logging.getLogger('gen')


def yield_upstreams():
  for line in sys.stdin.readlines():
    if line.isspace():
      continue

    match = re.match(PROXY_PASS_LINE_PATTERN, line)
    if match is None:
      logger.error('Invalid input format at %s', line)
      sys.exit(1)

    pair = match.groups()
    host, upstream = map(urlparse, pair)

    if host.scheme not in ['http', 'https']:
      logger.error('Wrong scheme in %s, should be http or https', host.geturl())
      sys.exit(1)

    upstream.name = hashlib.sha1(line).hexdigest()
    yield (host, upstream)


def upstreams_conf(upstreams):
  for host, upstream in upstreams:
    yield 'upstream %s { server %s; }' % (upstream.name, upstream.netloc)

  yield 'map $host $upstream {'
  for host, upstream in upstreams:
    yield '    %s "%s";' % (host.hostname, upstream.name)
  yield '}'


def domains(upstreams, scheme, prefix=''):
  upstreams = filter(lambda (host, u): host.scheme == scheme, upstreams)
  for host, u in upstreams:
    yield prefix + host.hostname


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('action', choices=['upstreams', 'http', 'https', 'certbot'])
  args = parser.parse_args()

  upstreams = list(yield_upstreams())
  if args.action == 'upstreams':
    print '\n'.join(upstreams_conf(upstreams))

  elif args.action == 'http':
    print ' '.join(domains(upstreams, 'http'))

  elif args.action == 'https':
    print ' '.join(domains(upstreams, 'https'))

  elif args.action == 'certbot':
    print ' '.join(domains(upstreams, 'https', '-d '))
