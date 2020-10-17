import argparse
import requests_cache

import swapi
import printer
import filters

parser = argparse.ArgumentParser(description='Get Star Wars data from SWAPI')
parser.add_argument('--format', choices=['json', 'text', 'list'], default='text', help='output format')
parser.add_argument('--fields', help='print only specific fields (coma-separated list). eg: \'name,population,terrain\'')
parser.add_argument('--filter', nargs=3, action='append', help='property operator value. eg: \'name = Tatooine\'')
parser.add_argument('--nocache', action='store_true', help='disable requests cache')
parser.add_argument('resource', help='resource to get')
args = parser.parse_args()

if not args.nocache:
    requests_cache.install_cache('.swcli_cache', backend='sqlite', expire_after=1800)

fields = []
if args.fields is not None:
    fields = list(map(str.strip, args.fields.split(sep=',')))

resources = swapi.getRoot()
if args.resource not in resources:
    print('Invalid resource name: \'%s\'. Available resources: [%s]' % (args.resource, ', '.join(resources)))
    exit(1)

data = swapi.getResource(args.resource)

if args.filter is not None:
    for filter in args.filter:
        data = filters.filter_data(data, filter)

printer.pprint(data, args.format, fields)
