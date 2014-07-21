#!/usr/bin/env python
import lib.torrent as torrent
import output.printer as printer
import output.fifo as fifo
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr,"Please specify torrent location"
        sys.exit(1)
    t = None
    try:
        t = torrent.create(sys.argv[1])
    except Exception, e:
        print >> sys.stderr,"Could not load torrent: %s" % e
        sys.exit(1)

    print >> sys.stderr,"Loading torrent..."
    t.makeSession()
    info = t.torrentInfo()
    print >> sys.stderr,"Name: %s" %(info.name())
    
    #t.startDownload(printer.Printer)
    t.startDownload(fifo.Fifo)
