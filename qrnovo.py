from ctypes import resize
from os import O_TRUNC, closerange
import cv2
from numpy.core.numeric import isclose
from pyzbar.pyzbar import decode
import json
import numpy as np

        

produtos = []
enderecos = []

lista = []




img = cv2.imread('./img/dinal.png')
height, width, channels = img.shape
barcodeList = decode(img)
if len(barcodeList) <= 4:
    for barcode in barcodeList:
        # (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")

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
    
        indexTemp and enderecos.pop(int(indexTemp))
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

cv2.imshow("camera",img)
key = cv2.waitKey(5)