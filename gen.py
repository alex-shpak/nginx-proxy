#!/usr/bin/python
import os
import argparse
import re
from urlparse import urlparse

def get_upstreams():
  if not os.environ.has_key('UPSTREAMS'):
    return dict()

  upstreams = dict()
  for line in os.environ['UPSTREAMS'].splitlines():
    pair = line.split('->')
    host, upstream = map(lambda it: urlparse(it.strip()), pair)
    upstream.name = re.sub('[:.]', '_', upstream.netloc)
    upstreams[host] = upstream

  return upstreams


def print_upstreams_file(upstreams):
  for host, upstream in upstreams.iteritems():
    print 'upstream %s { server %s; }' % (upstream.name, upstream.netloc)

  print 'map $host $upstream {'
  for host, upstream in upstreams.iteritems():
    print '    %s "%s";' % (host.hostname, upstream.name)
  print '}'


def print_domains(upstreams, scheme, prefix=''):
  http_domains = []
  for item in upstreams.keys():
    if item.scheme == scheme:
      http_domains.append(item.hostname)
  print ' '.join(
    [prefix + host for host in http_domains]
  )


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('action', choices=['upstreams', 'http', 'https', 'certbot'])
  args = parser.parse_args()

  upstreams = get_upstreams()
  if args.action == 'upstreams':
    print_upstreams_file(upstreams)

  elif args.action == 'http':
    print_domains(upstreams, 'http')

  elif args.action == 'https':
    print_domains(upstreams, 'https')

  elif args.action == 'certbot':
    print_domains(upstreams, 'https', '-d ')
