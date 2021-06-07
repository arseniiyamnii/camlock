#!/bin/python3
import face_recognition
import pygame
import pygame.camera
import os
from os import listdir
from os.path import isfile, join
import subprocess
import numpy
import sys
import signal
import time
import pickle


def change_delay(num):
    bashCommand = "gsettings set org.gnome.desktop.session idle-delay "
    subprocess.Popen((bashCommand+str(num)).split())
    subprocess.Popen(("xdotool mousemove_relative -- -5 -5").split())
    subprocess.Popen(("xdotool mousemove_relative -- 5 5").split())


def is_change_delay(lastres, rec):
    if lastres:
        time.sleep(2)

    if rec and not lastres:
        change_delay(300)
        print("i see you")
        lastres = True
    if not rec and lastres:
        change_delay(3)
        print("i cant see you")
        lastres = False
    return(lastres)


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


def make_photo_encod(cam):
    signal.signal(signal.SIGINT, signal_handler)
    img = cam.get_image()
    pygame.image.save(img, "Unknown.jpg")
    unknown_encoding = face_recognition.load_image_file(
        "Unknown.jpg")  # recognize photo
    os.remove("Unknown.jpg")
    return(unknown_encoding)


def init_cam():
    signal.signal(signal.SIGINT, signal_handler)
    pygame.camera.init()
    pygame.camera.list_cameras()  # Camera detected or not
    cam = pygame.camera.Camera("/dev/video0", (320, 240))
    cam.start()
    return(cam)


def img_rec(ownerencodings, image):
    try:
        unknown_encoding = face_recognition.face_encodings(image)[0]
        results = face_recognition.compare_faces(
            ownerencodings, unknown_encoding)
        try:
            best = results.index(True)+1
        except:
            best = False
    except:
        best = False
    return best


def main():
    # init camera
    cam = init_cam()
    lastres = is_change_delay(True, False)
    with open('owner.pickle', 'rb') as f:
        ownerencodings = pickle.load(f)

    while True:
        unknown_image = make_photo_encod(cam)  # recognize photo
        best = img_rec(ownerencodings, unknown_image)
        # print(best)
        if bool(best):
            while True:
                unknown_image = make_photo_encod(cam)
                best = img_rec([ownerencodings[best-1]], unknown_image)
                if best:
                    lastres = is_change_delay(lastres, True)
                if not best:
                    break
        else:
            lastres = is_change_delay(lastres, False)
        # time.sleep(1)


def scan():
    cam = init_cam()
    try:
        with open('owner.pickle', 'rb') as f:
            ownerencodings = pickle.load(f)
    except Exception:
        ownerencodings = []

    while True:
        print("Take photo? y/(any other key to stop): ")
        if input() == "y":
            known_image = make_photo_encod(cam)
            try:
                biden_encoding = face_recognition.face_encodings(known_image)[
                    0]
                ownerencodings.append(biden_encoding)
            except Exception:
                pass
            os.remove("Unknown.jpg")
        else:
            with open("owner.pickle", "wb") as f:
                pickle.dump(ownerencodings, f)
            break


if __name__ == "__main__":
    if sys.argv[1] == "start":
        main()
    if sys.argv[1] == "scan":
        scan()
