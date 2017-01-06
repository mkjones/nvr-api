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

    def getCameraInfos(self, cameraIds):

        csv = ','.join(cameraIds)
        infos = self._getJson('camera/'+csv, {})
        id2data = {}
        for info in infos['data']:
            camId = info['_id']
            id2data[camId] = info
        return id2data

    def getCameraInfo(self, cameraId):
        return self.getCameraInfos([cameraId])[cameraId]

    def disableCameraRecording(self, cameraId):
        info = self.getCameraInfo(cameraId)
        info['recordingSettings']['fullTimeRecordEnabled'] = False
        info['recordingSettings']['motionRecordEnabled'] = False
        return self._putJSON('camera/{id}'.format(id=cameraId), info)

    def enableCameraMotionRecording(self, cameraId):
        info = self.getCameraInfo(cameraId)
        info['recordingSettings']['fullTimeRecordEnabled'] = False
        info['recordingSettings']['motionRecordEnabled'] = True
        return self._putJSON('camera/{id}'.format(id=cameraId), info)

    def getRecordingIDs(self, time_back=86400):
        return self.getRecordingIDsForCamera(None, time_back)

    def getRecordingIDsForCamera(self, cameraID, time_back=86400):
        causes = ['motionRecording']
        now = time.time()
        start_time = int((now - time_back) * 1000)
        end_time = int(now * 1000)
        ids_only = True
        data = {'cause[]':causes,
                'startTime':start_time,
                'endTime':end_time,
                'idsOnly':ids_only,
                'sortBy':'startTime',
                'sort':'desc',
                }
        if cameraID is not None:
            data['cameras[]'] = cameraID
        raw_data = self._getJson('recording', data)
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
                            {'alpha':True})
        return raw_png

    def downloadRecording(self, recording_id:str):
        raw_mp4 = self._get('recording/{id}/download'.format(id=recording_id), {})
        prefix = "recording_"+recording_id
        with tempfile.NamedTemporaryFile(mode='w+b',
                                         suffix='.mp4',
                                         prefix=prefix,
                                         delete=False) as tmpfile:
            tmpfile.write(raw_mp4)
            return tmpfile.name


    def _makeurl(self, path:str, qps:dict):
        url = 'https://{host}:{port}/api/2.0/{path}?apiKey={apiKey}&{qps}'.format(
            host=self.host,
            port=self.port,
            path=path,
            apiKey=self.key,
            qps=urllib.parse.urlencode(qps, doseq=True)
            )

        return url

    def _get(self, path:str, qps:dict):
        url = self._makeurl(path, qps)
        ctx = ssl._create_unverified_context()

        request = urllib.request.Request(url=url)
        with urllib.request.urlopen(request, context=ctx) as result:
            return result.read()

    def _getJson(self, path:str, qps:dict):
        res = self._get(path, qps)
        return json.loads(res.decode('utf8'))

    def _putJSON(self, path:str, data):
        url = self._makeurl(path, {})
        ctx = ssl._create_unverified_context()

        dataStr = json.dumps(data).encode('utf8')
        headers = {'Content-Type':'application/json'}
        request = urllib.request.Request(url=url,
                                         method='PUT',
                                         headers=headers,
                                         data=dataStr)
        with urllib.request.urlopen(request, context=ctx) as result:
            return result.read()


if __name__ == '__main__':
    print(sys.argv)
    key = sys.argv[1]
    host = sys.argv[2]
    api = Api(key, host)
    api.bootstrap()
    pp.pprint(api.getCameraIDs())
    recordings = api.getRecordingIDs(86400 * 3)
    recordingInfos = {}
    for i in range(0, len(recordings), 20):
        recordingInfos.update(api.getRecordingInfos(recordings[i:i+20]))
    pp.pprint(recordings)
    for recording in recordings:
        cameraName = recordingInfos[recording]['meta']['cameraName']
        try:
            print("Getting recording motion %s for camera %s"
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
