import cherrypy
import dbus, time
import subprocess

class OMXPlayerAPI(object):	
    process = False
    dbus_prop = False
    dbus_key = False

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def open(self, file="/tmp/omxstream.fifo"):
        # stop any previous omxplayer
        if self.process:
            self.stop()

        # open omxplayer
        cmd = 'omxplayer -r -o hdmi "%s"' %(file)
        self.process = subprocess.Popen([cmd], shell=True)
        # wait for omxplayer to initialise
        done,retry=0,0
        while done==0:
            try:
                with open('/tmp/omxplayerdbus', 'r+') as f:
                    omxplayerdbus = f.read().strip()
                bus = dbus.bus.BusConnection(omxplayerdbus)
                object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
                self.dbus_prop = dbus.Interface(object,'org.freedesktop.DBus.Properties')
                self.dbus_key = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
                done=1
            except:
                retry+=1
                if retry >= 50:
                    self.stop()
                    return {"status" : False, "error": "Could not connect to OMXPlayer"}
        return {"status" : True}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def playpause(self):
        try:
            self.dbus_key.Pause()
            return {"status" : True}
        except Exception, e:
            return {"status" : False, "error" : str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop(self):
        if self.dbus_key:
            try:
                self.dbus_key.Stop()
            except:
                # Ignore error that dbus is broken
                pass
            self.dbus_key = False
        self.process.kill()
        self.process = False
        self.dbus_prop = False
        return {"status" : True}
