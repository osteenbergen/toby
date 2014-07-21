import cherrypy
import sys, dbus, time
import subprocess
from lib import vlc

class VLCPlayerAPI(object):	
    process = None
    torrent_api = None
    def __init__(self, torrent_api):
        self.torrent_api = torrent_api

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def open(self, file="/tmp/omxstream.fifo"):
        if not self.process:
            print >> sys.stderr, "file: %s" % file
            self.process = vlc.MediaPlayer('file://%s' % file) 
            self.process.set_fullscreen(1)
        return self.play()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def play(self):
        try:
            self.process.play()

            if self.process.will_play():
                return {"status" : True, "playable": self.process.will_play()}
            return {"status" : False}
        except Exception, e:
            return {"status" : False, "error" : str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pause(self):
        try:
            self.process.pause()

            if self.process.will_play():
                return {"status" : True, "playable": self.process.will_play()}
            return {"status" : False}
        except Exception, e:
            return {"status" : False, "error" : str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop(self):
        try:
            self.process.stop()
        except:
            pass
        self.torrent_api.stream_stop()
        self.process = None
        return {"status" : True}
