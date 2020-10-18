import requests
import requests_cache
import threading

from api import Api

class Swapi(Api):
    _page_size=10
    _base_url = 'https://swapi.dev/api/'

    def __init__(self, cache=True):
        if cache:
            requests_cache.install_cache('.swapi_cache', backend='sqlite', expire_after=3600)

    def do_request(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Unsucessful API response: %d' % response.status_code)

        try:
            return response.json()
        except ValueError as err:
            raise Exception('Invalid JSON response from API') from err

    def _get_last_page(self, count):
        return int(count / self._page_size) + (1 if count % self._page_size > 0 else 0)

    def _call_extend_result(self, url, results=[]):
        rjson = self.do_request(url)
        if 'results' in rjson:
            results.extend(rjson['results'])
        else:
            results.extend(rjson)

        return results

    def call(self, url):
        rjson = self.do_request(url)
        results = rjson

        if 'results' in rjson:
            results = rjson['results']

        if 'next' in rjson and rjson['next'] is not None:
            threads = []
            for page in range(2, self._get_last_page(rjson['count']) + 1):
                th = threading.Thread(target=self._call_extend_result, args=(url + ('?page=%d' % page), results))
                threads.append(th)
                th.start()
            for th in threads:
                th.join()

        return results

    def get_root(self):
        return self.call(self._base_url)

    def get_resource(self, resource, id=0):
        url = '%s%s/' % (self._base_url, resource)
        if id > 0:
            url = '%s%d/' % (url, id)
        return self.call(url)

