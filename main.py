#!/bin/python3
#IMPORTS#{{{
from threading import Thread
import pystray
from PIL import Image, ImageDraw
from pystray import Icon as trayicon, Menu as menu, MenuItem as item
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
import cv2
import logging
from systemd.journal import JournalHandler
from systemd import journal

#}}}
def create_image(color1, color2):
    width = 32
    height = 32
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def on_clicked(icon, item):
    global state
    state = not item.checked
    if state:
        print("stopping")
    else:
        print("running")

TIMESLEEP = 3
TIMEWAITBEFORESLEEP=15
TIMESCANIDLE=5
TIMEWAITIFGOOD=3

FIRST_DELAY = (subprocess.check_output("gsettings get org.gnome.desktop.session idle-delay".split())).split()[1].decode("utf-8")
lasttime = time.time()
# print(FIRST_DELAY)


def mouse_move(px=1):
    subprocess.Popen(("xdotool mousemove_relative -- -"+str(px)+" -"+str(px)).split())
    subprocess.Popen(("xdotool mousemove_relative -- "+str(px)+" "+str(px)).split())



def change_delay(num):
    # {{{
    bashCommand = "gsettings set org.gnome.desktop.session idle-delay "
    subprocess.Popen((bashCommand+str(num)).split())
    mouse_move()
    # }}}




def xsecidledelay(sec):
    timestart=time.time()# {{{
    while time.time()-timestart<sec:
        print(colored(str(time.time()-timestart)), "green")
        time.sleep(0.5)
        print(colored(str(subprocess.check_output("xssstate -i".split()).decode("utf-8")),"blue"))
        if int(subprocess.check_output("xssstate -i".split()).decode("utf-8")) < 2000:
            time.sleep(3)
            return(0)# }}}


def checkignore(cam):
    ssids = ['Yamnish2', 'Yamnish2_5G']
    try:
        ssid = subprocess.check_output("iwgetid".split()).decode("utf-8").split('"')[1]
    except:
        ssid = ""
    print(ssid)
    if ssid in ssids:
        cam.stop()
        while ssid in ssids:
            try:
                ssid = subprocess.check_output("iwgetid".split()).decode("utf-8").split('"')[1]
            except:
                ssid = ""
            print(ssid)
            time.sleep(20)
        cam.start()

def is_change_delay(lastres, rec, timestamp):
    global TIMESLEEP# {{{
    global TIMEWAITBEFORESLEEP
    global TIMESCANIDLE
    global TIMEWAITIFGOOD
    global FIRST_DELAY
    global lasttime
    # print(int(subprocess.check_output("xssstate -i".split()).decode("utf-8")))
    if lastres:
        time.sleep(TIMEWAITIFGOOD)
    if timestamp and time.time()-timestamp > TIMEWAITBEFORESLEEP+TIMESLEEP:
        xsecidledelay(TIMESCANIDLE)
        # if int(subprocess.check_output("xssstate -i".split()).decode("utf-8")) > 4000:
            # time.sleep(5)
    # elif timestamp != 0:
        # print(time.time()-timestamp)
    if rec and not lastres:
        change_delay(FIRST_DELAY)
        mouse_move()
        # print(colored(str(int(time.time()-lasttime)), "red"))
        # print(colored(str(datetime.datetime.now().time())[:-7], "green"), end="\r")
        # print(colored(str(datetime.datetime.now().time())[:-7], "green"), end=" ")

        lasttime=time.time()
        lastres = True
    if not rec and lastres:
        change_delay(TIMESLEEP)
        # print(colored(str(int(time.time()-lasttime)), "green"))
        # print(colored(str(datetime.datetime.now().time())[:-7], "red"), end="\r")
        # print(colored(str(datetime.datetime.now().time())[:-7], "red"), end=" ")

        lasttime=time.time()
        lastres = False
    return(lastres)# }}}


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")# {{{
    sys.exit(0)# }}}


def make_photo_encod(cam):
# {{{

    signal.signal(signal.SIGINT, signal_handler)
    # cam.start()

    # signal.signal(signal.SIGINT, signal_handler)

    # rec, img = cam.read()
    try:
        os.remove("/tmp/pycamUnknown.jpg")
    except:
        pass
    img = cam.get_image()
    # pygame.image.save(img, "/tmp/pycamUnknown.jpg")
    # os.remove("/tmp/pycamUnknown.jpg")
    img = cam.get_image()
    # pygame.image.save(img, "/tmp/pycamUnknown.jpg")
    # os.remove("/tmp/pycamUnknown.jpg")
    img = cam.get_image()
    pygame.image.save(img, "/tmp/pycamUnknown.jpg")
    # cv2.imwrite('/tmp/pycamUnknown.jpg', img)
    try:
        unknown_encoding = face_recognition.load_image_file(
        "/tmp/pycamUnknown.jpg")  # recognize photo
    except:
        unknown_encoding = False

    signal.signal(signal.SIGINT, signal_handler)
    # cam.stop()
    # os.remove("/tmp/pycamUnknown.jpg")
    return(unknown_encoding)
# }}}}}}


def init_cam():
    #{{{
    while True:
        try:
            signal.signal(signal.SIGINT, signal_handler)
            pygame.camera.init()
            pygame.camera.list_cameras()  # Camera detected or not
            cam = pygame.camera.Camera("/dev/video0", (320, 240))
            cam.start()
            # cam.stop()
            # cam = cv2.VideoCapture(0)
            signal.signal(signal.SIGINT, signal_handler)
            break
        except:
            print("cant init camera")
    return(cam)
    #}}}


def img_rec(ownerencodings, image):
    #{{{
    try:
        unknown_encoding = face_recognition.face_encodings(image)[0]
        result = face_recognition.face_distance(
            ownerencodings, unknown_encoding)
        # if result[result.argmax()]>xxx:
        print(float(result[result.argmin()]))
        if float(result[result.argmin()]) < 0.5:
            print("image comporing is ", float(result[result.argmin()]))
            best = int(result.argmin()+1)
        else:
            print("Got face, but not owner")
            best = False

    except:
        print("Error in comparing. Maybe no face")
        best = False
    # print(best)
    return(best)
    #}}}


def main(log):
    #{{{
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
        print("====================")
        print("Start test all images")
        unknown_image = make_photo_encod(cam)  # recognize photo
        best = img_rec(ownerencodings, unknown_image)
        if bool(best):
            print("Best image from array is ", str(best))
            print("start compairing with just image ", str(best))
            stopscanone=True
            mouse_move()
            lastres = is_change_delay(lastres, True, timestamp)
            timestamp = False
            while stopscanone:
                print("--------")
                unknown_image2 = make_photo_encod(cam)
                print("compare cam with", str(best))
                best2 = img_rec([ownerencodings[best-1]], unknown_image2)
                # print(best2)
                if best2:
                    log.info("sent to journal")
                    print("image same face")
                    lastres = is_change_delay(lastres, True, timestamp)
                    timestamp = False
                    checkignore(cam)
                else:
                    print("not same face")
                    stopscanone=False
                    break
                # time.sleep(4)
        else:
            print("all images wrong")
            if not timestamp:
                timestamp = time.time()
            lastres = is_change_delay(lastres, False, timestamp)
    #}}}


def scan():
    # {{{
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
    # }}}

def run_main():
    log = logging.getLogger('demo')
    log.addHandler(JournalHandler())
    log.setLevel(logging.INFO)
    main(log)

def run_icon():
    color1 = 'Red'
    color2 = 'Green'
    state = False
    image = create_image(color1, color2)
    item =item('stopping',on_clicked,checked=lambda item: state)
    icon = trayicon('test', image, menu=menu(item))
    icon.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "scan":
            scan()
    else:
        Thread(target = run_main).start()
        Thread(target = run_icon).start()
