# SWCLI (Star Wars CLI)

A CLI to fetch data from [swapi](https://swapi.dev/).

## Help
```
$ python swcli.py -h
usage: swcli.py [-h] [--format {json,text,list}] [--fields FIELDS] [--filter FILTER FILTER FILTER] [--nocache] resource

Get Star Wars data from SWAPI

positional arguments:
  resource              resource to get

optional arguments:
  -h, --help            show this help message and exit
  --format {json,text,list}
                        output format
  --fields FIELDS       print only specific fields (coma-separated list). eg: 'name,population,terrain'
  --filter FILTER FILTER FILTER
                        property operator value. eg: 'name = Tatooine'
  --nocache             disable requests cache
```

## Examples

Get all starships:
```
python swcli.py starships
```

Find all starships that appeared in the film "Return of the Jedi" (output in JSON format and selecting fields):
```
python swcli.py --format json --fields name,crew,hyperdrive_rating,manufacturer --filter films.title '=' 'Return of the Jedi' starships
```

Find all starships that have a `hyperdrive_rating` >= 1.0:
```
python swcli.py --format json --fields name,crew,hyperdrive_rating,manufacturer --filter hyperdrive_rating '>=' 1.0 starships
```

Find all starships that have a `crew` between 3 and 100:
```
python swcli.py --format json --fields name,crew,hyperdrive_rating,manufacturer --filter crew '>=' 3 --filter crew '<=' 100 starships
```

