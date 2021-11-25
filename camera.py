from ctypes import resize
from os import O_TRUNC, closerange
import cv2
from numpy.core.numeric import isclose
from pyzbar.pyzbar import decode
import json
import numpy as np

        






webcam = cv2.VideoCapture(0)

exp_val = 10

codec = 0x47504A4D # MJPG
webcam.set(cv2.CAP_PROP_FPS, 1.0)
webcam.set(cv2.CAP_PROP_FOURCC, codec)
webcam.set(cv2.CAP_PROP_EXPOSURE, exp_val)

if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()


        # cv2.fastNlMeansDenoisingColored(frame,frame,h=10,hColor=10,templateWindowSize=7,searchWindowSize=21)
        cv2.normalize(frame,frame,0,255,cv2.NORM_MINMAX)
        
        height, width, channels = frame.shape


        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.stylization(frame, sigma_s=60, sigma_r=0.07)

        frame = cv2.detailEnhance(frame, sigma_s=52, sigma_r=0.798)
        
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



        produtos = []
        enderecos = []
        lista = []

        barcodeList = decode(frame)
        if len(barcodeList) <= 4:
            for barcode in barcodeList:
                # (x, y, w, h) = barcode.rect
                (x, y, w, h) = barcode.rect
                barcodeData = barcode.data.decode("utf-8")
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 15)                   

                if 'QR01' in barcodeData:
                    produtos.append(barcode)
                elif 'QR02' in barcodeData:
                    enderecos.append(barcode)

                # print(x, y, w, h,barcodeData,len(barcodeData))
            for i,p in enumerate(produtos):
                print(i)
                (xp, yp, wp, hp) = p.rect
                distanciaTemp = ''
                enderecoTemp = ''
                indexTemp = ''
                list = {
                    'endereco':'',
                    'produto':p.data.decode("utf-8"),
                    'status':''
                }
                for j,e in enumerate(enderecos):
                    if j == 0:
                        (xe, ye, we, he) = e.rect
                        enderecoTemp = e.data.decode("utf-8")
                        distanciaTemp = ((xe - xp)**2 + (ye - yp )**2)**0.5
                        indexTemp = j
                    else:
                        (xe, ye, we, he) = e.rect
                        if ((xe - xp)**2 + (ye - yp )**2)**0.5 < distanciaTemp:
                            enderecoTemp = e.data.decode("utf-8")
                            distanciaTemp = ((xe - xp)**2 + (ye - yp )**2)**0.5
                            indexTemp = j

                if enderecoTemp[4:] in list['produto'][4:]: 
                    list['status'] = 'ok'
                else:
                    list['status'] = 'erro'

                list['endereco'] = enderecoTemp
                if (indexTemp != ''):
                    enderecos.pop(indexTemp)
                lista.append(list)
                    
        else:
            print('teste')

        if len(enderecos) > 0:
            for e in enderecos:
                list = {
                        'endereco':e.data.decode("utf-8"),
                        'produto':'',
                        'status':'Nao LEU'
                    }
                lista.append(list)

        print(lista)

        cv2.imshow("camera",frame)
        key = cv2.waitKey(5)