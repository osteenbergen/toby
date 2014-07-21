#!/usr/bin/env python
import cherrypy
import os
import simplejson as json
from api.torrent import TorrentAPI
from api.omxplayer import OMXPlayerAPI
from api.vlc import VLCPlayerAPI

def handle_error(*args, **kwargs):
    cherrypy.response.status = 500
    cherrypy.response.body = [json.dumps({"status": False})]
    return "error"

class Root(object):	
    pass

cherrypy.config.update({
        'request.error_response' : handle_error,
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : os.getcwd() + '/www',
        'tools.staticdir.index' : 'index.html',
    })
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 9091

torrent_api = TorrentAPI()
cherrypy.tree.mount(torrent_api, '/torrent')
#cherrypy.tree.mount(OMXPlayerAPI(), '/player')
cherrypy.tree.mount(VLCPlayerAPI(torrent_api), '/player')
cherrypy.quickstart(Root())
