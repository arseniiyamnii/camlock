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
from termcolor import colored
import datetime

TIMESLEEP = 2
FIRST_DELAY = (subprocess.check_output("gsettings get org.gnome.desktop.session idle-delay".split())).split()[1].decode("utf-8")
lasttime = time.time()
# print(FIRST_DELAY)


def change_delay(num):
    bashCommand = "gsettings set org.gnome.desktop.session idle-delay "
    subprocess.Popen((bashCommand+str(num)).split())
    subprocess.Popen(("xdotool mousemove_relative -- -5 -5").split())
    subprocess.Popen(("xdotool mousemove_relative -- 5 5").split())



def xsecidledelay(sec):
    timestart=time.time()
    while time.time()-timestart<sec:
        time.sleep(0.5)
        if int(subprocess.check_output("xssstate -i".split()).decode("utf-8")) < 2000:
            break


def is_change_delay(lastres, rec, timestamp):
    global TIMESLEEP
    global FIRST_DELAY
    global lasttime
    # print(int(subprocess.check_output("xssstate -i".split()).decode("utf-8")))
    if lastres:
        time.sleep(1)
    if timestamp and time.time()-timestamp > 5+TIMESLEEP:
        xsecidledelay(15)
        # if int(subprocess.check_output("xssstate -i".split()).decode("utf-8")) > 4000:
            # time.sleep(5)
    # elif timestamp != 0:
        # print(time.time()-timestamp)
    if rec and not lastres:
        change_delay(FIRST_DELAY)
        print(colored(str(int(time.time()-lasttime)), "red"))
        print(colored(str(datetime.datetime.now().time())[:-7], "green"), end="\r")
        print(colored(str(datetime.datetime.now().time())[:-7], "green"), end=" ")

        lasttime=time.time()
        lastres = True
    if not rec and lastres:
        change_delay(TIMESLEEP)
        print(colored(str(int(time.time()-lasttime)), "green"))
        print(colored(str(datetime.datetime.now().time())[:-7], "red"), end="\r")
        print(colored(str(datetime.datetime.now().time())[:-7], "red"), end=" ")

        lasttime=time.time()
        lastres = False
    return(lastres)


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


def make_photo_encod(cam):
    signal.signal(signal.SIGINT, signal_handler)
    img = cam.get_image()
    pygame.image.save(img, "/tmp/pycamUnknown.jpg")
    unknown_encoding = face_recognition.load_image_file(
        "/tmp/pycamUnknown.jpg")  # recognize photo
    os.remove("/tmp/pycamUnknown.jpg")
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
        result = face_recognition.face_distance(
            ownerencodings, unknown_encoding)
        # if result[result.argmax()]>xxx:
        # print(result)
        if float(result[result.argmin()]) < 0.5:
            best = result.argmin()+1
        else:
            best = False

    except:
        best = False
    # print(best)
    return best


def main():
    cam = init_cam()
    lastres = False  # is_change_delay(True, False)
    try:
        with open(os.path.expanduser("~")+'/.owner.pickle', 'rb') as f:
            ownerencodings = pickle.load(f)
        f.close()
    except:
        print("run -$./start-monitor.sh scan")
    timestamp = time.time()
    while True:
        unknown_image = make_photo_encod(cam)  # recognize photo
        best = img_rec(ownerencodings, unknown_image)
        # print(best)
        if bool(best):
            while True:
                unknown_image = make_photo_encod(cam)
                best = img_rec([ownerencodings[best-1]], unknown_image)
                if best:
                    lastres = is_change_delay(lastres, True, timestamp)
                    timestamp = False
                if not best:
                    break
        else:
            if not timestamp:
                timestamp = time.time()
            lastres = is_change_delay(lastres, False, timestamp)


def scan():
    cam = init_cam()
    try:
        with open(os.path.expanduser("~")+'/.owner.pickle', 'rb') as f:
            ownerencodings = pickle.load(f)
    except Exception:
        ownerencodings = []
    while True:
        print("Take photo? Enter/(any key to stop): ")
        try:
            y = input()
        except SyntaxError:
            y = ""
        if y == "":
            known_image = make_photo_encod(cam)
            try:
                biden_encoding = face_recognition.face_encodings(known_image)[0]
                ownerencodings.append(biden_encoding)
            except Exception:
                pass
        else:
            with open(os.path.expanduser("~")+"/.owner.pickle", "wb") as f:
                pickle.dump(ownerencodings, f)
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "scan":
            scan()
    else:
        main()
