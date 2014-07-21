from lib.piece_handler import PieceHandler
import sys

class Printer(PieceHandler):
    def __init__(self, torrent):
        super(Printer, self).__init__(torrent)
    
    def handle_piece(self, piece):
        sys.stdout.write(self.get_piece_bytes(piece))
