import os, sys, argparse, re, logging, hashlib
from urllib.parse import urlparse

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
    host, upstream = list(map(urlparse, pair))

    if host.scheme not in ['http', 'https']:
      logger.error('Wrong scheme in %s, should be http or https', host.geturl())
      sys.exit(1)

    name = hashlib.sha1(line.encode('utf-8')).hexdigest()
    yield (host, upstream, name)


def upstreams_conf(upstreams):
  for host, upstream, name in upstreams:
    yield 'upstream %s { server %s; }' % (name, upstream.netloc)

  yield 'map $host $upstream {'
  for host, upstream, name in upstreams:
    yield '    %s "%s";' % (host.hostname, name)
  yield '}'


def domains(upstreams, scheme, prefix=''):
  upstreams = filter(lambda line: line[0].scheme == scheme, upstreams)
  for host, _, _ in upstreams:
    yield prefix + host.hostname


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('action', choices=['upstreams', 'http', 'https', 'certbot'])
  args = parser.parse_args()

  upstreams = list(yield_upstreams())
  if args.action == 'upstreams':
    print('\n'.join(upstreams_conf(upstreams)))

  elif args.action == 'http':
    print(' '.join(domains(upstreams, 'http')))

  elif args.action == 'https':
    print(' '.join(domains(upstreams, 'https')))

  elif args.action == 'certbot':
    print(' '.join(domains(upstreams, 'https', '-d ')))
