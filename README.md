# rtsp_gstreamer


<div id="top"></div>





<div align="center">

  <h3 align="center">Stream iDS UEye through RTSP with GStreamer</h3>
</div>


<!-- ABOUT THE PROJECT -->
## About

This project uses GStreamer library to stream UEye camera.<br>

Tested with Gstreamer version 1.16.2 & 1.8 <br>
Tested on Ubuntu 20 & 18.<br>
Project was done @ ITRI.<br>
Nov 1 2021<br>
Maintained by kevinsagen47@gmail.com
<p align="right">(<a href="#top">back to top</a>)</p>


## Library Used

Library used in this project

* [Gstreamer 1.0](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c)
* [Gst library: gst-plugins-vision(branch: linux)](https://github.com/joshdoe/gst-plugins-vision/tree/linux)
* [iDS UEye driver](https://en.ids-imaging.com/downloads.html)

Miscellaneous: Introduction to Gstreamer https://gist.github.com/velovix/8cbb9bb7fe86a08fb5aa7909b2950259

<p align="right">(<a href="#top">back to top</a>)</p>


## Prerequisites
1. Install Gstreamer (Ubuntu or Debian)
  ```sh
  sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
  ```
2. Install iDS UEye Driver from iDS website https://en.ids-imaging.com/downloads.html 


## Install Gstreamer Plugin (Linux) 
For Windows, follow [this guide](https://github.com/joshdoe/gst-plugins-vision/tree/master)
1. Clone UEye library repo 
   ```sh
   apt-get install git cmake libgstreamer-plugins-base1.0-dev liborc-0.4-dev
   git clone https://github.com/joshdoe/gst-plugins-vision/tree/linux
   unzip gst-plugins-vision-linux.zip 
   cd gst-plugins-vision-linux
   mkdir build
   cd build
   cmake ..
   make
   make install
   make package
   ```
2. copy .so file to gstreamer library location (current directory: gst-plugins-vision-linux)
   ```sh
   cp build/sys/idsueye/libgstidsueye.so /usr/local/lib/gstreamer-1.0/
   ```
3. export library location (on gstreamer 1.8, you need to repeat this step everytime you reopen the terminal)
   ```js
   export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-1.0
   ```    
<p align="right">(<a href="#top">back to top</a>)</p>


## Hello World Gstreamer

Gstreamer camera sources:
- idsueyesrc  : UEye Camera
- v4l2src     : Webcam
- videotestsrc: video test signal

Example usage of Gstreamer (output test video)
```
gst-launch-1.0 videotestsrc ! decodebin ! videoconvert ! autovideosink
```
Stream webcam video
```
gst-launch-1.0 v4l2src! decodebin ! videoconvert ! autovideosink
```
Check if gstreamer ueye library is installed
```
gst-inspect-1.0 idsueyesrc
```
If installed correctly, output must be:
```
Factory Details:
  Rank                     none (0)
  Long-name                IDS uEye Video Source
  Klass                    Source/Video
  Description              IDS uEye framegrabber video source
  Author                   Joshua M. Doe <oss@nvl.army.mil>

Plugin Details:
  Name                     idsueye
  Description              IDS uEye frame grabber source
  Filename                 /usr/local/lib/gstreamer-1.0/libgstidsueye.so
  Version                  HEAD-HASH-NOTFOUND
  License                  LGPL
  Source module            gst-plugins-vision package
  Binary package           gst-plugins-vision
  Origin URL               Unknown package origin

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseSrc
                         +----GstPushSrc
```
Stream ueye camera with command line
```
gst-launch-1.0 idsueyesrc ! decodebin ! videoconvert ! autovideosink
```
Stream ueye camera with Gstreamer in Python [code](https://github.com/kevinsagen47/rtsp_gstreamer/blob/main/local_stream_ueye.py)

Stream ueye camera with OpenCV (without Gstreamer) [code courtesy of Yang-Yi Zheng](https://github.com/kevinsagen47/rtsp_gstreamer/blob/main/itri_ueye.py)


## Stream on RTSP 

###  Host
Python [code](https://github.com/kevinsagen47/rtsp_gstreamer/blob/main/rtsp_host.py)

### Client
Play on the same device client with Gstreamer (latency <1s)
```
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/stream1 latency=0 ! decodebin ! autovideosink
```

Play on a different device local network client with Gstreamer (latency <1s)
```
gst-launch-1.0 rtspsrc location=rtsp://<HOST IP Address>:8554/stream1 latency=0 ! decodebin ! autovideosink
```

Play with OpenCV (latency >2s)[code courtesy of Claire](https://github.com/kevinsagen47/rtsp_gstreamer/blob/main/rtsp_stream_client.py) (change "video_path" variable to host's IP address)

Play with VLC (UEye camera not supported)
```
vlc -v rtsp://127.0.0.1:8554/stream1
```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Issues -->
## Known issues

- Unable to stream UEye camera through VLC, probably due to unsuported codec (error: only real/helix rtsp servers supported for now)
- Currently unable to change camera setting , i.e. ISO, white balance, exposure (probably can be changed through config.ini file)

<p align="right">(<a href="#top">back to top</a>)</p>

