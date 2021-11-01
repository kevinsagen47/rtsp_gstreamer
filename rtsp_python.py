#!/usr/bin/env python

#RECEIVER TERMINAL COMMAND
#vlc -v rtsp://127.0.0.1:8554/stream1
#only real/helix rtsp servers supported for now
#gst-launch-1.0 playbin uri=rtsp://127.0.0.1:8554/stream1 #LATENCY IS 2 SECONDS
#gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/stream1 latency=0 ! decodebin ! autovideosink #0 LATENCY


import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib

loop = GLib.MainLoop()
Gst.init(None)

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        #set mp4 file path to filesrc's location property
        src_demux = "filesrc location=/home/kevin/Documents/Work/bao.mp4 ! qtdemux name=demux"
        h264_transcode = "demux.video_0"
        #uncomment following line if video transcoding is necessary
        #h264_transcode = "demux.video_0 ! decodebin ! queue ! x264enc"
        #pipeline = "{0} {1} ! queue ! rtph264pay name=pay0 config-interval=1 pt=96".format(src_demux, h264_transcode)
        
        #pipeline = " idsueyesrc blocksize=1000096 !  videobalance brightness=0.2 ! videoconvert ! queue ! video/x-raw,format=I420,width=2048, height=1088 ! videoscale ! x264enc speed-preset=superfast tune=zerolatency bitrate=500 ! rtph264pay name=pay0 config-interval=1 pt=96"
        encode = "x264enc speed-preset=ultrafast tune=zerolatency byte-stream=true threads=1 key-int-max=0 intra-refresh=true pass=qual ! rtph264pay name=pay0 config-interval=1 pt=96"
        pipeline = " idsueyesrc blocksize=1000096 !  videobalance brightness=0.2 ! videoconvert ! queue ! video/x-raw,format=I420,width=2048, height=1088 ! videoscale ! " +encode
        pipeline = " v4l2src ! videoconvert ! queue ! video/x-raw,format=I420 ! videoscale ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay name=pay0 config-interval=1 pt=96"
        print ("Element created: " + pipeline)
        return Gst.parse_launch(pipeline)

class GstreamerRtspServer():
    def __init__(self):
        self.rtspServer = GstRtspServer.RTSPServer()
        factory = TestRtspMediaFactory()
        factory.set_shared(True)
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory("/stream1", factory)
        self.rtspServer.attach(None)

if __name__ == '__main__':
    s = GstreamerRtspServer()
    loop.run()