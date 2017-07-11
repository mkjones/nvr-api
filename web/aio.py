import aiohttp
from aiohttp import web
import nvrsym.NvrApi as NvrApi
import sys
import tornado.escape as es


async def index(req):
    api = await get_api()
    cameras = await api.getCameraIDs()
    ret = ''
    for camid in cameras.keys():
        name = cameras[camid]
        link = "/cam?id={id}".format(id=camid)
        row = "<div class='cameraName'><a href='{link}'>{name}</a></div>"
        ret += row.format(link=link, name=es.xhtml_escape(name))
    return web.Response(body=ret, content_type='text/html')

async def cam(req):
    api = await get_api()
    cameraID = req.query['id']
    recordingIDs = await api.getRecordingIDsForCamera(cameraID, 7*86400)
    ret = ''
    for recid in recordingIDs:
        path = "/motion?id={id}".format(id=recid)
        row = "<img width='180' height='100' src='{path}' />".format(path=path)

        vidpath = "/video?id={id}".format(id=recid)
        link = "<a href='{vidpath}'>{img}</a>".format(vidpath=vidpath, img=row)
        ret += link
    return web.Response(body=ret, content_type='text/html')

async def motion(req):
    api = await get_api()
    recid = req.query['id']
    png = await api.getRecordingMotion(recid)
    return web.Response(body=png, content_type='image/png')

async def video(req):
    api = await get_api()
    recid = req.query['id']
    tmpfile = await api.downloadRecording(recid)
    bytes = open(tmpfile, 'rb').read()

    return web.Response(body=bytes, content_type='video/mp4')

async def get_api():
    global global_client
    if global_client is None:
        key = sys.argv[1]
        host = sys.argv[2]
        global_client = NvrApi.Api(key, host)
        await global_client.bootstrap()

    return global_client

app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/cam', cam)
app.router.add_get('/motion', motion)
app.router.add_get('/video', video)

client_session=aiohttp.ClientSession()
global_client = None

web.run_app(app, host='127.0.0.1', port=9990)
