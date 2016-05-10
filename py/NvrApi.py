import json
import urllib.parse
import urllib.request
import sys
import ssl
import pprint as pp

class Api:

    GET_BUFFER_LEN = 100 * 1024

    def __init__(self, key:str, host:str, port:int=7443):
        self.key = key
        self.host = host
        self.port = port

    def bootstrap(self):
        raw_json = self._get('bootstrap')
        raw_data = json.loads(raw_json)
        data = raw_data['data'][0]
        return data

    def camera(self):
        raw_json = self._get('camera')
        raw_data = json.loads(raw_json)
        return raw_data

    def getCameraIDs(self):
        """ Get a map<cam_id, cam_name> """
        bs = self.bootstrap()
        cams = bs['cameras']
        ret = {}
        for cam in cams:
            cam_id = cam['_id']
            cam_name = cam['deviceSettings']['name']
            ret[cam_id] = cam_name
        return ret


    def _get(self, path):
        url = 'https://{host}:{port}/api/2.0/{path}?apiKey={apiKey}'.format(
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
    pp.pprint(api.bootstrap())
    pp.pprint(api.getCameraIDs())
    #pp.pprint(api.camera())
