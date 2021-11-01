from threading import Thread
from time import sleep
import gi
import getch

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")

from gi.repository import Gst, GLib,GstApp

_ = GstApp

Gst.init(None)

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()


#src = "v4l2src! decodebin ! videoconvert ! autovideosink"   # WORKS
src = 'idsueyesrc! videobalance brightness=0.2 ! decodebin ! videoconvert ! autovideosink' # WORKS

pipeline = Gst.parse_launch(src)
pipeline.set_state(Gst.State.PLAYING)

count = 0
try:
    while True:
        sleep(0.01)
        count+=1
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
thread.join()

