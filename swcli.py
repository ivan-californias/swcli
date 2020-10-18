import argparse
import sys

from swapi import Swapi
from filters import Filters
import printer

def swcli(resource, filter_cmds=None, cache=True):
    api = Swapi(cache)
    resources = api.get_root()
    if resource not in resources:
        raise Exception('Invalid resource name: \'%s\'. Available resources: [%s]' % (resource, ', '.join(resources)))

    data = api.get_resource(resource)

    if filter_cmds:
        filters = Filters(api)
        for f in filter_cmds:
            data = filters.filter_data(data, field_name=f[0], operator=f[1], value=f[2])

    return data

def main():
    parser = argparse.ArgumentParser(description='Get Star Wars data from SWAPI')
    parser.add_argument('--format', choices=['json', 'text', 'list'], default='text', help='output format')
    parser.add_argument('--fields', help='print only specific fields (coma-separated list). eg: \'name,population,terrain\'')
    parser.add_argument('--filter', nargs=3, action='append', help='field_name operator value. eg: \'name = Tatooine\'')
    parser.add_argument('--nocache', action='store_true', help='disable requests cache')
    parser.add_argument('resource', help='resource to get')
    args = parser.parse_args()

    fields = []
    if args.fields is not None:
        fields = list(map(str.strip, args.fields.split(sep=',')))

    try:
        data = swcli(args.resource, filter_cmds=args.filter, cache=not(args.nocache))
    except Exception as err:
        print("ERROR: %s" % err, file=sys.stderr)
        exit(1)

    if not data:
        print("No results", file=sys.stderr)
        exit(1)

    printer.print_data(data, args.format, fields)

if __name__ == '__main__':
    main()
