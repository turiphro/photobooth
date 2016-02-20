#!/usr/bin/env python5
# Simple photo booth software
# using Polaroid PoGo, webcam (opencv), and input buttons (via MakeyMakey)

import cv2
import os, sys
import time, datetime

import polaroid

WEBCAM_DEVICE = 1
STORAGE_DIR = 'storage'

# NOTE: printing ratio may be different; may need to crop


def putText(img, text, location, positive=True):
    """UI helper function for adding text to image"""
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
    printer = polaroid.Polaroid()
    printer.connect()

    # open webcam and UI
    cap = cv2.VideoCapture(WEBCAM_DEVICE)
    screen = 'photo_booth'
    cv2.namedWindow(screen, cv2.WND_PROP_FULLSCREEN)

    # show webcam and wait for user input
    while True:
        ret, frame = cap.read()
        img = frame
        img_ui = img.copy()
        putText(img_ui, "TAKE", 'left_button', True)
        cv2.imshow(screen, img_ui)
        keypress = cv2.waitKey(10)

        if keypress == 32: # space: take photo
            # take snapshot, wait for user input
            img_ui = img.copy()
            putText(img_ui, "PRINT", 'left_button', True)
            putText(img_ui, "RETAKE", 'right_button', False)
            cv2.imshow(screen, img_ui)
            keypress = cv2.waitKey(0)

            if keypress == 32: # space: print
                # save snapshot, send to printer
                datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(os.getcwd(), STORAGE_DIR, datestr + ".jpg")
                cv2.imwrite(filename, img)

                # send to printer
                printer.send_image(filename)

                # countdown while printing (scientifically proven waiting time)
                for i in range(48, 0, -1):
                    time.sleep(1)
                    img_ui = img.copy()
                    putText(img_ui, "PRINTING ({})".format(i), 'centre', True)
                    cv2.imshow(screen, img_ui)
                    cv2.waitKey(1)
            else:
                continue # retake

        if keypress == 27: # ESC: exit
            break
