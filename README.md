
[![codecov](https://codecov.io/gh/ivan-californias/swcli/branch/master/graph/badge.svg?token=ZSF51NA6X5)](undefined)

# SWCLI (Star Wars CLI)

A CLI to fetch data from [swapi](https://swapi.dev/).

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
                        field_name operator value. eg: 'name = Tatooine'
  --nocache             disable requests cache
```

#### --fields

This argument works as a whitelist of the fields that are desired on the output. Works for all the output formats.

Names specified in this whitelist should be properties at the top level of the requested **resource**. Nested properties are currently not supported.

Can specify any number of fields separated by comma `,`:
```
--fields name,terrain,population
```

#### --filter

It is posible to filter the data by a set given coditions.

Each `--filter` argument should receive exactly 3 parameters:

- `field_name`: Name of the field/property of the resource to compare when filtering data. Can refer to nested objects
  with a dot `.`. Example: `films.title`, films is at the top level while title is a property of `films`.
- `operator`: Operator to use in the comparision function. One of the following:
  - `=`: **Equal**, `field_name` and `value` values are the same.
  - `!=`: **Not equal**, `field_name` and `value` values are different.
  - `~>`: **Contained in**, `field_name` value is contained in `value` (strings).
  - `<~`: **Contains**, `field_name` value contains `value` (strings).
  - `>`: **Greater than**, greater than or equal to, `field_name` value is greater than `value` (numbers).
  - `>=`: **Greater than or equal to**, `field_name` value is greater than or equal to `value` (numbers).
  - `<`: **Less than**, `field_name` value is less than `value` (numbers).
  - `<=`: **Less than or equal to**, `field_name` value is less than or equal to `value` (numbers).
  - _Note_: It is recomended to enclose this parameter with quotation marks. eg. `'>='`
- `value`: The value to be used to compare against the value of `field_name`

Example:
```
--filter hyperdrive_rating '>=' 1.0
```

Example with a nested property:
```
--filter films.title '=' 'Return of the Jedi'
```

It is also possible to apply multiple filters:
```
--filter crew '>=' 3 --filter crew '<=' 100
```

## Requirements

_Recomended: Create a virtual environment_
```
python -m venv env
source env/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

**Tested with Python 3.8.5**

