#!/bin/python3
import face_recognition
import pygame
import pygame.camera
from os import listdir
from os.path import isfile, join
import subprocess
import numpy

pygame.camera.init()
pygame.camera.list_cameras() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
onlyfiles = [f for f in listdir("owner") if isfile(join("owner", f))]
bashCommand = "gsettings set org.gnome.desktop.session idle-delay "
lastres = False
result = True
while True:
    img = cam.get_image()
    pygame.image.save(img,"Unknown.jpg")
    unknown_image = face_recognition.load_image_file("Unknown.jpg")
    ownerencodings = []
    for i in onlyfiles:
        try:
            known_image = face_recognition.load_image_file("owner/"+i) #get image one
            biden_encoding = face_recognition.face_encodings(known_image)[0]
            ownerencodings.append(biden_encoding)
        except:
            pass
    try:        
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0] # test image one
        results = face_recognition.compare_faces(ownerencodings, unknown_encoding)
        result = bool(numpy.any(results))
        # print(type(result))
        # print(result)
    except:
        result = False
    if not result and lastres:
        lastres = False
        process = subprocess.Popen((bashCommand+"3").split(), stdout=subprocess.PIPE)
        print("stop")
    elif result and not lastres:
        lastres = True
        process = subprocess.Popen((bashCommand+"300").split(), stdout=subprocess.PIPE)
        print("start")

