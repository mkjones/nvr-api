import json
import urllib.parse
import urllib.request
import sys
import ssl
import pprint as pp
import time
import tempfile

class Api:

    GET_BUFFER_LEN = 100 * 1024

    def __init__(self, key:str, host:str, port:int=7443):
        self.key = key
        self.host = host
        self.port = port

    def bootstrap(self):
        raw_data = self._getJson('bootstrap', {})
        data = raw_data['data'][0]
        return data

    def camera(self):
        raw_data = self._getJson('camera', {})
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

    def getRecordingIDs(self, time_back=86400):
        causes = ['fullTimeRecording', 'motionRecording']
        now = time.time()
        start_time = int((now - time_back) * 1000)
        end_time = int(now * 1000)
        ids_only = True
        raw_data = self._getJson('recording', {'cause[]':causes,
                                           'startTime':start_time,
                                           'endTime':end_time,
                                           'idsOnly':ids_only,
                                           'sortBy':'startTime',
                                           'sort':'desc',
                                           })
        return raw_data['data']

    def getRecordingInfos(self, recordingIDs:list):
        csv = ','.join(recordingIDs)
        infos = self._getJson('recording/'+csv, {})['data']
        id2data = {}
        for info in infos:
            id2data[info['_id']] = info

        return id2data

    def getRecordingMotion(self, recording_id:str):
        raw_png = self._get('recording/{id}/motion'.format(id=recording_id),
                            {'alpha':False})
        return raw_png

    def downloadRecording(self, recording_id:str):
        raw_mp4 = self._get('recording/{id}/download'.format(id=recording_id), {})
        print("mp4 length: %d bytes" % len(raw_mp4))
        prefix = "recording_"+recording_id
        with tempfile.NamedTemporaryFile(mode='w+b',
                                         suffix='.mp4',
                                         prefix=prefix,
                                         delete=False) as tmpfile:
            tmpfile.write(raw_mp4)
            return tmpfile.name

    def _get(self, path:str, qps:dict):
        url = 'https://{host}:{port}/api/2.0/{path}?apiKey={apiKey}&{qps}'.format(
            host=self.host,
            port=self.port,
            path=path,
            apiKey=self.key,
            qps=urllib.parse.urlencode(qps, doseq=True)
            )

        print(url)
        ctx = ssl._create_unverified_context()

        request = urllib.request.Request(url=url)
        with urllib.request.urlopen(request, context=ctx) as result:
            return result.read()

    def _getJson(self, path:str, qps:dict):
        res = self._get(path, qps)
        return json.loads(res.decode('utf8'))

if __name__ == '__main__':
    print(sys.argv)
    key = sys.argv[1]
    host = sys.argv[2]
    api = Api(key, host)
    api.bootstrap()
    pp.pprint(api.getCameraIDs())
    recordings = api.getRecordingIDs()
    recordingInfos = api.getRecordingInfos(recordings)
    pp.pprint(recordings)
    for recording in recordings:
        cameraName = recordingInfos[recording]['meta']['cameraName']
        try:
            print("Getting recording %s for camera %s"
                  % (recording, cameraName))
            png = api.getRecordingMotion(recording)
        except Exception as e:
            print('error with recording ' + recording)
            print(e)
            continue
        filename = '/tmp/recordings/{camera}_{id}.png'.format(camera=cameraName, id=recording)
        f = open(filename, 'wb')
        f.write(png)
        f.close()
        print
    #pp.pprint(api.camera())
