import ConnectivityTester as ct
import NvrApi
import time
import sys
import asyncio

def log(message):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print("{time}:\t{message}".format(time=now, message=message))
    sys.stdout.flush()


async def run(api, ips, cameras):
    testers = [ct.Tester(ip) for ip in ips]
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
                await asyncio.sleep(1)
            else:
                timesince = "Time since last API call: {timesince}; up IPs: {up}".format(
                    timesince=int(timeSinceLastAPI),
                    up=','.join(upIPs)
                    )
                if disableRecording:
                    log("Disabling recording.  {timesince}"
                        .format(timesince=timesince))
                    [await api.disableCameraRecording(c) for c in cameras]
                else:
                    log("Enabling recording.  {timesince}".format(timesince=timesince))
                    [await api.enableCameraMotionRecording(c) for c in cameras]
                lastAPITime = time.time()

            prevDisableRecording = disableRecording
        except Exception as e:
            print("error in loop: ")
            print(e)

if __name__ == '__main__':
    key = sys.argv[1]
    host = sys.argv[2]
    api = NvrApi.Api(key, host)

    ips = sys.argv[3].split(',')

    cameras = sys.argv[4].split(',')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(api, ips, cameras))
    loop.close()
