#!/usr/bin/env python3
import cv2
import os, sys
import time, datetime
import polaroid

WEBCAM_DEVICE = 1
STORAGE_DIR = 'storage'


def putText(img, text, location, positive=True):
    font = cv2.FONT_HERSHEY_DUPLEX
    fsize = 2
    colour = (0, 255, 0) if positive else (255, 0, 0)
    if location == 'left_button':
        cv2.putText(img, text, (0, img.shape[0] - 10),
                    font, fsize, colour)
    elif location == 'right_button':
        cv2.putText(
            img, text,
            (int(img.shape[1] - 40*len(text)), int(img.shape[0] - 10)),
            font, fsize, colour)
    elif location == 'centre':
        cv2.putText(
            img, text,
            (int(img.shape[1] / 2 - 20*len(text)), int(img.shape[0] / 2)),
            font, fsize, colour)


if __name__ == '__main__':
    # open bluetooth connection (keep open)
    device = polaroid.Polaroid()

    # open webcam
    cap = cv2.VideoCapture(WEBCAM_DEVICE)
    screen = 'photo_booth'
    cv2.namedWindow(screen, cv2.WND_PROP_FULLSCREEN)
    while True:
        ret, frame = cap.read()
        img = frame
        cv2.imshow(screen, img)
        keypress = cv2.waitKey(10)
        print(keypress)
        if keypress == 32: # space
            print("SNAPSHOT")
            img_ui = img.copy()
            putText(img_ui, "PRINT", 'left_button', True)
            putText(img_ui, "RETAKE", 'right_button', False)
            cv2.imshow(screen, img_ui)
            keypress = cv2.waitKey(0)
            if keypress == 32: # space
                print("SAVING AND PRINTING")
                datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                cv2.imwrite(os.path.join(STORAGE_DIR, datestr, ".png"), img)
                img_ui = img.copy()
                putText(img_ui, "PRINTING", 'centre', True)
                cv2.imshow(screen, img_ui)
                cv2.waitKey(1)
                time.sleep(4)
            continue
        if keypress == 27: # ESC
            break

    #   show webcam
    #   if keypress ' ':
    #     take picture
    #     print("OK?")
    #     if keypress ' ':
    #       save photo
    #       send to printer
    #       upload to instagram / twitter
    #       show loader (printing time) -> or can get status via bt?
    
    # decisions:
    # - can use cheese, check for photo in dir (but no cancel)

