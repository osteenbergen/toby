import libtorrent as lt
import thread
import sys
import time

class PieceHandler(object):
    def __init__(self, torrent):
        print >> sys.stderr, "Init piece handler..."
        if not torrent:
            self.cancel()
        self.torrent = torrent
        self.cache = {}
        self.loop()
        
    def loop(self):
        while self.torrent.end_piece >= self.torrent.current_piece:
            self.get_current_piece()
        
    def get_current_piece(self):        
        if not hasattr(self.torrent,"torrent_handle") or not self.torrent.torrent_handle:
            raise Exception("No torrent started")

        # Do we have it in our cache?
        if self.torrent.current_piece in self.cache:
            ret = self.cache[self.torrent.current_piece]
            cache[self.torrent.current_piece] = 0
            return ret

        while True:
            s = self.torrent.torrent_handle.status()
            if s.pieces[self.torrent.current_piece]:
                break
            time.sleep(.1)
            if self.torrent.cancel_download:
                thread.exit()

        self.torrent.torrent_handle.read_piece(self.torrent.current_piece);

        while True:
            piece = self.torrent.session.pop_alert()
            if isinstance(piece, lt.read_piece_alert):
                if piece.piece == self.torrent.current_piece:
                    self.torrent.current_piece = self.torrent.current_piece + 1
                    return self.handle_piece(piece)
                else:
                    self.cache[piece.piece] = piece.buffer
                    return self.get_current_piece()
            time.sleep(.1)
            
            if self.torrent.cancel_download:
                thread.exit()
     
    def handle_piece(self, piece):
        print piece.piece
        
    def get_piece_bytes(self, piece):
        buf = piece.buffer
        if piece.piece == self.torrent.start_piece:
            buf = buf[self.torrent.start_byte:]
        if piece.piece == self.torrent.end_piece:
            buf = buf[:self.torrent.end_byte]
        return buf
       
    def cancel(self):
        print >> sys.stderr, "Could not handle pieces..."
        if self.torrent:
            self.torrent.cancel()
        thread.exit()
        
