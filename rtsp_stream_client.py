import time
import cv2

video_path = "rtsp://192.168.8.101:8554/stream1"
SHOW_LIVEVIEW = True
SHOW_INFO_IN_TERMINAL = True
SHOW_INFO_IN_LIVEVIEW = True

def write_text(img, text):
    # text = "FONT_HERSHEY_DUPLEX"
    position = (20, 100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 1
    color = (0, 255, 255)
    thickness = 2
    lineType =  cv2.LINE_AA
    cv2.putText(img, text, position, font, size, color, thickness, lineType)

    return img


if __name__ == '__main__':
    vid = cv2.VideoCapture(video_path)
    Ts = time.time()
    cnt = 0
    before_time = 0

    while(True):
        img = vid.read()[1]

        shape = img.shape
        shape = (int(shape[1]), int(shape[0]))

        cnt = cnt + 1
        time_pass = time.time()-Ts
        info_text = "Time: {:.2f}, Frame count: {:08d}, fps: {:.2f}, fps_one: {:.2f}".format(time_pass, cnt, cnt/time_pass, 1/(time_pass-before_time))

        if SHOW_INFO_IN_LIVEVIEW:
            img = write_text(img, info_text)

        if SHOW_INFO_IN_TERMINAL:
            print(f"\r{info_text}", end = "")

        before_time = time.time()-Ts

        img = cv2.resize(img, shape, interpolation=cv2.INTER_CUBIC)

        if SHOW_LIVEVIEW:
            img = cv2.resize(img, shape, interpolation=cv2.INTER_CUBIC)
            cv2.namedWindow('rtsp', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('rtsp', shape[0], shape[1])
            cv2.imshow('rtsp', img)
            cv2.waitKey(1)