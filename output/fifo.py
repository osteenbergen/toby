from lib.piece_handler import PieceHandler
import thread
import sys
import os
import stat

class Fifo(PieceHandler):
    def __init__(self, torrent):
        self.filename = "/tmp/omxstream.fifo"
        self.torrent = torrent
        print "INIT: %s" % self.filename
        try:
            os.mkfifo(self.filename)
        except Exception, e:
            print e
            pass
        print "Open FIFO"
        try:
            self.fifo = open(self.filename, 'w')
        except Exception, e:
            print "Error: %s" %s
        print "Get SUper"
        super(Fifo, self).__init__(torrent)
    
    def handle_piece(self, piece):
        try:
            self.fifo.write(self.get_piece_bytes(piece))
            self.fifo.flush()
        except:
            self.torrent.cancel()
            # Fifo is closed stop this
            thread.exit()
            
