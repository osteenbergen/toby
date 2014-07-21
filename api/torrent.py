import cherrypy
import thread
from lib.torrent import Torrent
from output.fifo import Fifo

class TorrentAPI(object):	
    torrent = False
    streaming = False
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def load(self, location):
        try:
            self.torrent = Torrent(location, tmpdir="/tmp")
            self.streaming = False
            self.torrent.makeSession()
            self.torrent_thread = thread.start_new_thread(self.torrent.startDownload, ())
            return {"status": True}
        except Exception, e:
            return {"status": False, "error" :e}


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def info(self):
        if self.torrent:
            info = self.torrent.torrentInfo(donotload=True)
            if not info:
                return {"status": True,
                        "fetching" : True}
            return {
                    "status" : True, 
                    "streaming" : self.streaming,
                    "comment" : info.comment(),
                    "creator" : info.creator(),
                    "size" : info.total_size(),
                    "pieces" : info.num_pieces(),
                    "piece_length" : info.piece_length(),
                    "name" : info.name(),
                    #"metadata" : info.metadata(),
                    "progress" : self.torrent.download_status()}
        else:
            return {"status" : False, "error" : "No torrent loaded"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stream(self):
        if hasattr(self.torrent, "torrent_handle") and self.torrent.torrent_handle:
            if self.torrent.cancel_download:
                self.torrent.resume()

            self.fifo_thread = thread.start_new_thread(Fifo,(self.torrent,))
            self.streaming = True
            return {"status" : True}
        else:
            return {"status": False, "error" : "No torrent started"}

    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stream_stop(self):
        self.torrent.cancel()
        self.streaming = False;

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop(self):
        self.stream_stop()
        del self.torrent
        self.torrent = False
        return {"status" : True}
