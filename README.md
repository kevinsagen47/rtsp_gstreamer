# rtsp_gstreamer


<div id="top"></div>





<div align="center">

  <h3 align="center">Stream iDS UEye to RTSP with GStreamer</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project uses GStreamer library to stream UEye camera.<br>
Project was done @ ITRI.<br>
Primarily tested on Ubuntu 20 & 18.<br>
Nov 1 2021<br>

<p align="right">(<a href="#top">back to top</a>)</p>



### Library Used

Library used in this project

* [Gstreamer 1.0](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c)
* [Gst library: gst-plugins-vision(branch: linux)](https://github.com/joshdoe/gst-plugins-vision/tree/linux)
* [iDS UEye driver](https://en.ids-imaging.com/downloads.html)
  

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation

1. Install Gstreamer (Ubuntu or Debian
  ```sh
  sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
  ```
2. Install iDS UEye Driver from iDS website https://en.ids-imaging.com/downloads.html 

3. Clone UEye library repo
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
4. copy .so file to gstreamer library location (current directory: gst-plugins-vision-linux)
   ```sh
   cp build/sys/idsueye/libgstidsueye.so /usr/local/lib/gstreamer-1.0/
   ```
5. export library location (on ubuntu 18, you need to repeat this step)
   ```js
   export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-1.0
   ```

    
<p align="right">(<a href="#top">back to top</a>)</p>


## Hello Gstreamer
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
Stream from ueye video
```
gst-launch-1.0 idsueyesrc ! decodebin ! videoconvert ! autovideosink
```


<!-- USAGE EXAMPLES -->
## Usage

#Test gstreamer library



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- Issues -->
## Issues

- Unable to stream through VLC, probably due to unsuported codec (error: only real/helix rtsp servers supported for now)
- Currently unable to change camera setting , i.e. ISO, white balance, exposure (probably can be changed through config.ini file)

<p align="right">(<a href="#top">back to top</a>)</p>

