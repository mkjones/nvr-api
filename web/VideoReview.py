import tornado.ioloop
import tornado.web
import tornado.escape as es
import sys
import nvr.NvrApi as NvrApi

# Displays a list of cameras
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        cameras = global_api.getCameraIDs()
        for camid in cameras.keys():
            name = cameras[camid]
            link = "/camera/?id={id}".format(id=camid)
            row = "<div class='cameraName'><a href='{link}'>{name}</a></div>"
            self.write(row.format(link=link, name=es.xhtml_escape(name)))

# Displays a grid of motion images for a given camera
class CameraHandler(tornado.web.RequestHandler):

    def get(self):
        cameraID = self.get_argument('id')
        recordingIDs = global_api.getRecordingIDsForCamera(cameraID, 7*86400)
        for recid in recordingIDs:
            path = "/motion/?id={id}".format(id=recid)
            row = "<img width='180' height='100' src='{path}' />".format(path=path)

            vidpath = "/video/?id={id}".format(id=recid)
            link = "<a href='{vidpath}'>{img}</a>".format(vidpath=vidpath, img=row)
            self.write(link)

# Displays the motion image for a given recording
class MotionHandler(tornado.web.RequestHandler):

    def get(self):
        recid = self.get_argument('id')
        motion_png = global_api.getRecordingMotion(recid)
        self.set_header('Content-Type', 'image/png')
        self.write(motion_png)

# Proxies the video content for the given recording
class VideoHandler(tornado.web.RequestHandler):

    def get(self):
        recid = self.get_argument('id')
        tmpfile = global_api.downloadRecording(recid)
        bytes = open(tmpfile, 'rb').read()
        self.set_header('Content-Type', 'video/mp4')
        self.set_header('Content-Length', len(bytes))
        self.write(bytes)

def get_api():
    key = sys.argv[1]
    host = sys.argv[2]
    api = NvrApi.Api(key, host)
    api.bootstrap()

    return api

global_api = None
if __name__ == "__main__":
    global_api = get_api()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/camera/", CameraHandler),
        (r"/motion/", MotionHandler),
        (r"/video/", VideoHandler),
    ])



    # now start up the app itself
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
