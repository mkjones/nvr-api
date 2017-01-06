import ConnectivityTester as ct
import NvrApi
import time
import sys

def log(message):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print("{time}:\t{message}".format(time=now, message=message))
    sys.stdout.flush()


if __name__ == '__main__':
    ips = [
        # put IPs of phones you want to watch for here
        ]
    cameras = [
        # put IDs of cameras you want to turn recording on / off for here
        ]
    testers = [ct.Tester(ip) for ip in ips]

    key = sys.argv[1]
    host = sys.argv[2]
    api = NvrApi.Api(key, host)

    prevDisableRecording = None
    lastAPITime = time.time()
    while True:
        try:
            upIPs = [t.ip for t in testers if t.isUp() ]
            disableRecording = len(upIPs) > 0
            timeSinceLastAPI = time.time() - lastAPITime
            if disableRecording == prevDisableRecording and timeSinceLastAPI < 60:
                # if we're in the same state as before and we recently
                # made an API call, then don't bother making another one.
                time.sleep(1)
            else:
                timesince = "Time since last API call: {timesince}; up IPs: {up}".format(
                    timesince=int(timeSinceLastAPI),
                    up=','.join(upIPs)
                    )
                if disableRecording:
                    log("Disabling recording.  {timesince}"
                        .format(timesince=timesince))
                    [api.disableCameraRecording(c) for c in cameras]
                else:
                    log("Enabling recording.  {timesince}".format(timesince=timesince))
                    [api.enableCameraMotionRecording(c) for c in cameras]
                lastAPITime = time.time()

            prevDisableRecording = disableRecording
        except Exception as e:
            print("error in loop: ")
            print(e)
