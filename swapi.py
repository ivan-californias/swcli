import requests

BASE_URL = 'https://swapi.dev/api/'

def call(url):
    try:
        response = requests.get(url)
        rjson = response.json()
    except Error as err:
        print('Error getting data from API:')
        print(err)
        exit(2)

    results = rjson

    if 'results' in rjson:
        results = rjson['results']

    if 'next' in rjson and rjson['next'] is not None:
        next_results = call(rjson['next'])
        results.extend(next_results)

    return results

def getRoot():
    return call(BASE_URL)

def getResource(resource, id=0):
    url = '%s%s/' % (BASE_URL, resource)
    if id > 0:
        url = '%s%d/' % (url, id)
    return call(url)

