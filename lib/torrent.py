import libtorrent as lt
import os
import urllib
import hashlib
import thread
import time
import sys

class Torrent:
    
    def __init__(self, location, tmpdir='/tmp/omxstream'):
        self.location = location
        self.tmpdir = tmpdir
        try:
            os.makedirs(self.tmpdir)
        except OSError, e:
            # Folder already exists
            pass
        self.session = lt.session()
        # where should we store the torrent
        self.torrent_params = { 'save_path': self.tmpdir}
        self.torrent_handle = None
        self.cancel_download = False
        
        # Position / Piece information
        self.current_piece = 0
        self.start_piece = 0
        self.start_byte = 0
        self.end_piece = 0
        self.end_byte = 0
        # Buffer to let the downloading continue while we handle the pieces
        self.piece_buffer_size = 40*1024*1024
        self.piece_in_buffer=0
        self.file_index = -1

    def makeSession(self):
        self.session.start_dht(None)
        self.session.add_dht_router("router.bittorrent.com", 6881)
        self.session.add_dht_router("router.utorrent.com", 6881)
        self.session.add_dht_router("router.bitcomet.com", 6881)
        self.session.listen_on(6881, 6891)
        self.session.set_alert_mask(lt.alert.category_t.storage_notification)

    def torrentInfo(self, donotload=False):
        if not self.session:
            raise Exception("Need session first")
        # URL:
        # http://piratebaytorrents.info/5579280/Big_Buck_Bunny_(1080p).ogv.5579280.TPB.torrent
        if not donotload and len(self.location)>4 and self.location[0:4] == 'http':
            # Create tmp torrent file in the tmp dir
            dest = self.tmpdir + '/' + hashlib.md5(self.location).hexdigest() + '.torrent'
            urllib.urlretrieve(self.location, dest)
            # Set the location to this file
            self.location = dest
        # Magnet: 
        # magnet:?xt=urn:btih:e541adf64e5d10c0827579447948aefba651e4f4&dn=Big+Buck+Bunny+%281080p%29.ogv&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337
        if len(self.location)>6 and self.location[0:6] == 'magnet':
            if donotload and not self.torrent_handle:
                print >> sys.stderr, "NOT Loading"
                return None

            if not self.torrent_handle or not hasattr(self,"magnet"):
                self.magnet = lt.add_magnet_uri(self.session, self.location, self.torrent_params)
                print >> sys.stderr, 'Downloading metadata...'
                while (not self.magnet.has_metadata()): time.sleep(1)
                self.torrent_handle = self.magnet
            # Return info
            return self.magnet.get_torrent_info()
        elif self.location:
            try:
                return lt.torrent_info(self.location)
            except:
                pass
        return None
    
    def chooseFile(self, strategy='max', info=None):
        # Get the info if needed
        if not info:
            info = self.torrentInfo()
        
        # Scan all files
        sizes = []
        i = 0
        for f in info.files():
            sizes.append(f.size)
            i=i+1
         
        # Possible strategies   
        if strategy == 'max':
            file_index = sizes.index(max(sizes))
         
        # Store the winner   
        self.file_index = file_index
        return file_index
      
    def startDownload(self, info=None):
        if self.file_index == -1:
            self.chooseFile()
        if not info:
            info = self.torrentInfo()
        if not self.torrent_handle:
            self.torrent_params['ti'] = info
            self.torrent_handle = self.session.add_torrent(self.torrent_params)

        #Initialize pieces
        self.update_buffer(info)
            
        self.torrent_handle.set_sequential_download(True)

        #self.torrent_handle.set_max_connections(40)
        self.torrent_handle.set_max_uploads(10)
        
        # Disable download of all pieces and assign
        for i in range(info.num_pieces()):
            self.torrent_handle.piece_priority(i,0)
            
        f = info.files()[self.file_index]
        self.start_piece = f.offset / info.piece_length()
        self.end_piece = (f.offset + f.size) / info.piece_length()
        self.start_byte = f.offset % info.piece_length() #how many bytes need to be removed from the 1st piece
        self.end_byte = ((f.offset + f.size) % info.piece_length()) #how many bytes need we keep from the last piece
        self.piece_in_buffer = self.piece_buffer_size / info.piece_length()
        
        self.current_piece = self.start_piece
        
        self.update_buffer(info)
        print >> sys.stderr, "Started Download"
        while self.current_piece != self.end_piece:
            self.update_buffer(info)
            time.sleep(1)
            if self.cancel_download:
               break
    
    def update_buffer(self, info = None):
        if not info:
            info = self.torrentInfo()
        
        prio = self.torrent_handle.piece_priorities()
        s = self.torrent_handle.status()

        for i in range(self.current_piece, self.current_piece + self.piece_in_buffer):
            # Mark these as maximum priority, ignore availability
            self.torrent_handle.piece_priority(i,7)

        downloading = 0
        for piece in range(self.start_piece,self.end_piece+1):
            if prio[piece] != 0 and s.pieces[piece]==False:
                downloading = downloading+1
                
            #outside of buffer, but we have already downloaded some piece after our current piece
            if prio[piece] == 0 and downloading < self.piece_in_buffer:
                self.torrent_handle.piece_priority(piece,1)
                downloading = downloading+1
    
    def download_status(self):
        state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

        if not self.torrent_handle:
            return None;

        s = self.torrent_handle.status()

        sys.stdout.flush()
        l = ''
        i = 0
        completed = 0
        for p in s.pieces:
            if i >= self.start_piece and i <= self.end_piece:
                if p == True:
                    l = l + '1'
                    completed = completed+1
                if p == False:
                    l = l + '0'
            i = i+1
        progress = 0
        if i!=0:
            progress = 1.*completed/i
                
        buffer_pieces = s.pieces[self.current_piece:self.current_piece + self.piece_in_buffer]

        status = {
                "paused":s.paused, 
                "completed":progress * 100, 
                "down": s.download_rate / 1000, 
                "up": s.upload_rate / 1000, 
                "peers": s.num_peers, 
                "current_piece" : s.pieces[self.current_piece],
                "start_piece" : self.start_piece,
                "needed_piece" : self.current_piece,
                "availability" : self.torrent_handle.piece_availability(),
                "buffer":{
                    "status" : sum(buffer_pieces) == self.piece_in_buffer,
                    "pieces" : buffer_pieces
                },
                "seeds": s.num_seeds}
        return status
    
    def resume(self):
        print >> sys.stderr, "Resume download..."
        self.cancel_download = False
        if self.torrent_handle:
            self.torrent_handle.resume()

    def cancel(self):
        print >> sys.stderr, "Pause download..."
        self.cancel_download = True
        self.current_piece = self.start_piece
        if self.torrent_handle:
            self.torrent_handle.pause()
    
    def __str__(self):
        obj = {'location': self.location}
        return str(obj)
