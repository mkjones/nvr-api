import json
import urllib.parse
import urllib.request
import sys
import ssl

class Api:

    GET_BUFFER_LEN = 100 * 1024

    def __init__(self, key:str, host:str, port:int=7443):
        self.key = key
        self.host = host
        self.port = port

    def bootstrap(self):
        data = self._get('bootstrap')
        return json.loads(data)

    def _get(self, path):
        url = 'https://{host}:{port}/api/2.0/{path}?apiKey=%s'.format(
            host=self.host,
            port=self.port,
            path=path,
            apiKey=self.key
            )

        print(url)
        ctx = ssl._create_unverified_context()

        request = urllib.request.Request(url=url)
        with urllib.request.urlopen(request, context=ctx) as result:
            return result.read(Api.GET_BUFFER_LEN).decode('utf8')

if __name__ == '__main__':
    print(sys.argv)
    key = sys.argv[1]
    host = sys.argv[2]
    api = Api(key, host)
    print(api.bootstrap())
