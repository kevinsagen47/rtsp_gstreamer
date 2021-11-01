#===========================================================================#
# Date: 2021/08/02                                                          #
# Maintainer: Yang-Yi Zeng, Liang-Fan Luo, Justin Chang                     #
# This program is a light function for IDS camera opening                   #
#===========================================================================#

from pyueye import ueye
import numpy as np
import cv2
import sys
import ctypes
import os


IS_SUCCESS = ueye.IS_SUCCESS


# Save camera information in a .ini file
def saveCamInfo(hCam, path):
    pParam = ueye.wchar_p()
    pParam.value = path
    nRet = ueye.is_ParameterSet(hCam, ueye.IS_PARAMETERSET_CMD_SAVE_FILE, pParam, ueye.UINT(0))
    if nRet != ueye.IS_SUCCESS:
        print("E: Camera Information Save Failed in function: saveCamInfo")

# Load camera information from a .ini file
def loadCamInfo(hCam, path):
    pParam = ueye.wchar_p()
    pParam.value = path
    nRet = ueye.is_ParameterSet(hCam, ueye.IS_PARAMETERSET_CMD_LOAD_FILE, pParam, ueye.UINT(0))
    if nRet != ueye.IS_SUCCESS:
        print("E: Fail to Load Camera Information from {}".format(path))

# Save camera information in a .ini file
def saveCamInfoToMem(hCam):
    pParam = ueye.wchar_p()
    pParam.value = path
    nRet = ueye.is_ParameterSet(hCam, ueye.IS_PARAMETERSET_CMD_SAVE_EEPROM, ueye.UINT(0), ueye.UINT(0))
    if nRet != ueye.IS_SUCCESS:
        print("E: Camera Information Save Failed in function: saveCamInfoToMem")

#Load camera information from memory
def loadCamInfoFromMem(hCam):
    nRet = ueye.is_ParameterSet(hCam, ueye.IS_PARAMETERSET_CMD_LOAD_EEPROM, ueye.UINT(0), ueye.UINT(0))
    if nRet != ueye.IS_SUCCESS:
        print("E: Fail to Load Camera Information from EEPROM")

# Get range of fps, nRange: True-supported limit value, False-current value
def getFPS(hCam, nRange = False):
    if nRange:
        minfps = ctypes.c_double(0)
        maxfps = ctypes.c_double(0)
        intervalfps = ctypes.c_double(0)
        nRet = ueye.is_GetFrameTimeRange(hCam, maxfps, minfps, intervalfps)
        if nRet != ueye.IS_SUCCESS:
            print("is_GetFrameTimeRange ERROR")
        fpsR = [1/minfps.value, 1/maxfps.value]
    else:
        fpsR = ctypes.c_double(0)
        nRet = ueye.is_GetFramesPerSecond(hCam, fpsR)
        fpsR = fpsR.value
        if nRet != ueye.IS_SUCCESS:
            print("is_GetFramePerSecond ERROR")
        

    return fpsR

# FPS setting
def setFPS(hCam, FPS):
    FPS = ctypes.c_double(FPS)
    New_FPS = id(FPS)
    New_FPS = ctypes.c_double(New_FPS)
    nRet = ueye.is_SetFrameRate(hCam, FPS, New_FPS)
    if nRet != ueye.IS_SUCCESS:
       print("is_SetFrameRate ERROR")

# Get exposure time, nRange: True-supported limit value, False-current value
def getExposureTime(hCam, nRange = False):
    minExposure = ctypes.c_double(0)
    maxExposure = ctypes.c_double(0)
    Exposure_time_size = ueye.sizeof(minExposure)
    if nRange:
        nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN, minExposure, Exposure_time_size)
        if nRet != ueye.IS_SUCCESS:
            print("is_Exposure_GET_MIN ERROR")
        nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX, maxExposure, Exposure_time_size)
        if nRet != ueye.IS_SUCCESS:
            print("is_Exposure_GET_MAX ERROR")
        exposureR = [minExposure.value, maxExposure.value]
    else:
        exposureR = ctypes.c_double(0)
        nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, exposureR, Exposure_time_size)
        exposureR = exposureR.value
        if nRet != ueye.IS_SUCCESS:
            print("is_Exposure_GET ERROR")
        
    return exposureR

# Exposure Setting
def setExposureTime(hCam, exposureTime):
    Exposure_time = ctypes.c_double(exposureTime)
    Exposure_time_size = ueye.sizeof(Exposure_time)
    nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, Exposure_time, Exposure_time_size)
    if nRet != ueye.IS_SUCCESS:
       print("is_Exposure ERROR")

# Get sharpness
def getSharpness(hCam, roi):
    # Set Sharpness Region of Interest
    measureSharpnessInfo = ueye.MEASURE_SHARPNESS_AOI_INFO()
    measureSharpnessInfo.u32NumberAOI   = 0
    measureSharpnessInfo.rcAOI.s32X     = roi[0]
    measureSharpnessInfo.rcAOI.s32Y     = roi[1]
    measureSharpnessInfo.rcAOI.s32Width = roi[2]
    measureSharpnessInfo.rcAOI.s32Height = roi[3]
    nRet = ueye.is_Measure(hCam, ueye.IS_MEASURE_CMD_SHARPNESS_AOI_SET, measureSharpnessInfo, ueye.sizeof(measureSharpnessInfo))
    # Get sharpness of active image memory
    measureSharpnessInfo.pcImageMem = None
    nRet = ueye.is_Measure(hCam, ueye.IS_MEASURE_CMD_SHARPNESS_AOI_INQUIRE, measureSharpnessInfo, ueye.sizeof(measureSharpnessInfo));
    if nRet == IS_SUCCESS:
        fSharpness = measureSharpnessInfo.u32SharpnessValue
        return fSharpness
    else:
        print("Cannot get sharpness in function: \"getSharpness\"")
    
# AWB setting
def setAWB(hCam, nEnable = 0, types = 2):
    nEnable = ueye.UINT(nEnable) # 0: disable(default), 1: enable, 2:enable once
    nEnable_size = ueye.sizeof(nEnable)
    nRet = ueye.is_AutoParameter(hCam, ueye.IS_AWB_CMD_GET_ENABLE, nEnable, nEnable_size)
    if nEnable:
        nType = ueye.UINT(types) # 1: Greyworld, 2: Color temperature(default)
        nType_size = ueye.sizeof(nType)
        nRet = ueye.is_AutoParameter(hCam, ueye.IS_AWB_CMD_SET_TYPE, nType, nType_size)
    
# Save image in .bmp file
def saveImg(name, img):
    path = os.path.join(os.getcwd(), "image")
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(path + "/" + name + ".bmp", img)

# Get frame (BGR type)
def getFrame(MemPtr, width, height, nBitsPerPixel, pitch, copy=False):
    # Extract the data of our image memory
    bytes_per_pixel = int(nBitsPerPixel / 8)
    array = ueye.get_data(MemPtr, width, height, nBitsPerPixel, pitch, copy=copy)
    # ...reshape it in an numpy array...
    frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))
    
    return frame

# Open camera and initialize
def openCamera(dev_id = 0, colormode = 1, exposureTime = 30, fps = 25, showInfo = False):
    ## variables
    hCam = ueye.HIDS(dev_id)            #0: first available camera;  1-254: The camera with the specified camera ID
    sInfo = ueye.SENSORINFO()
    cInfo = ueye.CAMINFO()
    MemPtr = ueye.c_mem_p()
    MemID = ueye.int()
    rectAOI = ueye.IS_RECT()
    pitch = ueye.INT()
    nBitsPerPixel = ueye.INT(24)        #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
    channels = 3                        #3: channels for color mode(RGB); take 1 channel for monochrome
    m_nColorMode = ueye.INT(colormode)  # Y8/RGB16/RGB24/REG32
    bytes_per_pixel = int(nBitsPerPixel / 8)

    Exposure_time = exposureTime        # unit: ms (0.009 ~ 38.721)
    FPS = fps                           #(0.5 ~ 25.80) 
    
    
    ## Starts the driver and establishes the connection to the camera
    nRet = ueye.is_InitCamera(hCam, None)
    if nRet != ueye.IS_SUCCESS:
        print("is_InitCamera ERROR")

    # Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
    nRet = ueye.is_GetCameraInfo(hCam, cInfo)
    if nRet != ueye.IS_SUCCESS:
        print("is_GetCameraInfo ERROR")

    # You can query additional information about the sensor type used in the camera
    nRet = ueye.is_GetSensorInfo(hCam, sInfo)
    if nRet != ueye.IS_SUCCESS:
        print("is_GetSensorInfo ERROR")

    nRet = ueye.is_ResetToDefault(hCam)
    if nRet != ueye.IS_SUCCESS:
        print("is_ResetToDefault ERROR")

    # Set display mode to DIB
    nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB) 


    ## Set the right color mode
    if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
        # setup the color depth to the current windows setting
        ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        if showInfo == True:
            print("IS_COLORMODE_BAYER: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t", bytes_per_pixel)
            print()

    elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
        # for color camera models use RGB32 mode
        m_nColorMode = ueye.IS_CM_BGRA8_PACKED
        nBitsPerPixel = ueye.INT(32)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        if showInfo == True:
            print("IS_COLORMODE_CBYCRY: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t", bytes_per_pixel)
            print()

    elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
        # for color camera models use RGB32 mode
        m_nColorMode = ueye.IS_CM_MONO8
        nBitsPerPixel = ueye.INT(8)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        if showInfo == True:
            print("IS_COLORMODE_MONOCHROME: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t", bytes_per_pixel)
            print()

    else:
        # for monochrome camera models use Y8 mode
        m_nColorMode = ueye.IS_CM_MONO8
        nBitsPerPixel = ueye.INT(8)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        if showInfo == True:
            print("IS_COLORMODE_MONOCHROME: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t", bytes_per_pixel)
            print() 


    ## Can be used to set the size and position of an "area of interest"(AOI) within an image
    nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
    if nRet != ueye.IS_SUCCESS:
        print("is_AOI ERROR")

    width = rectAOI.s32Width
    height = rectAOI.s32Height

    # Set Framerate 
    minfps = ctypes.c_double(0)
    maxfps = ctypes.c_double(0)
    intervalfps = ctypes.c_double(0)
    nRet = ueye.is_GetFrameTimeRange(hCam, maxfps, minfps, intervalfps)
    if nRet != ueye.IS_SUCCESS:
        print("is_GetFrameTimeRange ERROR")
    fpsR = [1/minfps.value, 1/maxfps.value]
    FPS = ctypes.c_double(FPS)
    New_FPS = id(FPS)
    New_FPS = ctypes.c_double(New_FPS)
    nRet = ueye.is_SetFrameRate(hCam, FPS, New_FPS)
    if nRet != ueye.IS_SUCCESS:
        print("is_SetFrameRate ERROR")
    
    # Set Exposure
    Exposure_time = ctypes.c_double(Exposure_time)
    Exposure_time_size = ueye.sizeof(Exposure_time)
    minExposure = ctypes.c_double(0)
    maxExposure = ctypes.c_double(0)

    nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN, minExposure, Exposure_time_size)
    if nRet != ueye.IS_SUCCESS:
        print("is_Exposure_GET_MIN ERROR")
    nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX, maxExposure, Exposure_time_size)
    if nRet != ueye.IS_SUCCESS:
        print("is_Exposure_GET_MAX ERROR")
    exposureR = [minExposure.value, maxExposure.value]
    nRet = ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, Exposure_time, Exposure_time_size)
    if nRet != ueye.IS_SUCCESS:
        print("is_Exposure ERROR")
    
    # Prints out some information about the camera and the sensor
    if showInfo == True:
        print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
        print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
        print("Maximum image width:\t", width)
        print("Maximum image height:\t", height)
        print("Minimum FPS:\t\t", 1/minfps.value)
        print("Maximum FPS:\t\t", 1/maxfps.value)
        print("Current FPS:\t\t", New_FPS.value)
        print("Minimum Exposure Time:\t", minExposure.value)
        print("Maximum Exposure Time:\t", maxExposure.value)
        print("Current Exposure Time:\t", Exposure_time.value)
        print() 

    ## Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
    nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, MemPtr, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_AllocImageMem ERROR")
    else:
        # Makes the specified image memory the active memory
        nRet = ueye.is_SetImageMem(hCam, MemPtr, MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_SetImageMem ERROR")
        else:
            # Set the desired color mode
            nRet = ueye.is_SetColorMode(hCam, m_nColorMode)

    # Activates the camera's live video mode (free run mode)
    nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
    if nRet != ueye.IS_SUCCESS:
        print("is_CaptureVideo ERROR")

    # Enables the queue mode for existing image memory sequences
    nRet = ueye.is_InquireImageMem(hCam, MemPtr, MemID, width, height, nBitsPerPixel, pitch)
    if nRet != ueye.IS_SUCCESS:
        print("is_InquireImageMem ERROR")
    else:
        print("Camera on, Press Esc to leave the program")
        # print("Press q to leave the program") # for opencv use

    return (hCam, nRet, MemPtr, MemID, nBitsPerPixel, pitch, rectAOI)

# Close camera & Release memory
def closeCamera(hCam, MemPtr, MemID):
    # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
    ueye.is_FreeImageMem(hCam, MemPtr, MemID)
    # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
    ueye.is_ExitCamera(hCam)

if __name__ == "__main__":
    # example to use the py file
    (hCam, nRet, MemPtr, MemID, nBitsPerPixel, pitch, rectAOI) = openCamera(dev_id = 0, colormode = 1, exposureTime = 30, fps = 60, showInfo = True)
    width = rectAOI.s32Width
    height = rectAOI.s32Height
    
    #---------------------------------------------------------------------------------------------------------------------------------------
    # Include image data processing here
    # # FPS setting ====================================================================
    # current_fps = getFPS(hCam, nRange=True)
    # print(current_fps)
    # setFPS(hCam, FPS=30)
    # Exposure Setting
    # ==================================================================================
    # # Exposure Setting ===============================================================
    # current_exposureTime = getExposureTime(hCam, nRange=False)
    # print(current_exposureTime)
    # setExposureTime(hCam, exposureTime=30)
    # ==================================================================================
    # # Auto White Balance Setting =====================================================
    # # Default: OFF
    # setAWB(hCam, nEnable=1,types=2)
    # ==================================================================================
    # Load Camera Information from memory =================================================================
    # loadCamInfoFromMem(hCam)
    #---------------------------------------------------------------------------------------------------------------------------------------
    
    while(nRet == IS_SUCCESS):
        frame = getFrame(MemPtr, width, height, nBitsPerPixel, pitch, copy=False)
        # # Save image
        # saveImg(name, frame)
    
        # # Get sharpness
        #roi = [x, y, w, h]
        # sharpness = getSharpness(hCam, roi)
        # print(sharpness)
    
        # Resize the image by a half
        frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
    
        #...and finally display it
        cv2.imshow("PuEye_OpenCV", frame)

        # Press Esc if you want to end the loop
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    # Close the cmaera and release the memory
    closeCamera(hCam, MemPtr, MemID)

    # Destroys the OpenCv windows
    cv2.destroyAllWindows()
    
