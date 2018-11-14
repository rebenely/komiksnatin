import cv2, sys
from os import listdir
from os.path import isfile, join

path = "C:\\RE\\School\\CS 165\\project\\komiksnatin\\komikrepo\\static\\images\\komikrepo"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

print(onlyfiles)
for image_name in onlyfiles:
    if "jpg" in image_name:
        image = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)
        image_hdpi = cv2.resize(image, (317,475))
        print(image_name, image_hdpi.size)
        cv2.imwrite(image_name, image_hdpi)
