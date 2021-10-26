
from ctypes import resize
from os import O_TRUNC, closerange
import cv2
from numpy.core.numeric import isclose
from pyzbar.pyzbar import decode
import json
import numpy as np


        
while True:
    img = cv2.imread('./img/dirnal.png')
    height, width, channels = img.shape
    for barcode in decode(img):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        cv2.rectangle(img, (x, y), (x + w, y + h), (0,255, 0), 2)

        print(barcodeData)

    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break