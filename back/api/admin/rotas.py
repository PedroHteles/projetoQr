from functools import partial

from sqlalchemy.dialects.mysql.base import RESERVED_WORDS
from api import engine
from api.admin.models import projetoEstoque
from flask import Flask,request,jsonify 
from sqlalchemy.sql import select
import cv2
from pyzbar.pyzbar import decode
import numpy as np


leituraProduto = []
leituraEndereco = []
validado = []
webcam = cv2.VideoCapture(0)


def lerqr(imagem,height,width):
    start_point = (int(width / 6), int(height  / 12))
    end_point = (int(width / 1.25), int(height / 1.05))
    cv2.rectangle(imagem, start_point, end_point,(255,0,0),2)
    
    for barcode in decode(imagem):
        barcodeData = barcode.data.decode("utf-8")
        (x, y, w, h) = barcode.rect
        leituraArea = x < (end_point[0]-w) and x > start_point[0] and y < (end_point[1]-h) and y > start_point[1] 
        try:
            if leituraArea:
                
                if validado !=[]:
                    for i in validado:
                        if barcodeData in i:
                            return barcodeData

                if len(barcodeData) ==16 and leituraEndereco !=[]:
                    if barcodeData not in leituraProduto:
                        leituraProduto.append(barcodeData)
                    pass
                elif  len(barcodeData) ==12:
                    if barcodeData not in leituraEndereco:
                        leituraEndereco.append(barcodeData)
                    pass

                if len(leituraEndereco) + len(leituraProduto) == len(decode(imagem)) and len(decode(imagem)) >2:
                    print(' mais de 2 qr encontrado')
                    valor = (leituraEndereco,leituraProduto)
                    return valor
                elif len(decode(imagem)) ==1:
                    if barcodeData in leituraEndereco and len(leituraProduto) ==1 or len(leituraProduto) >1:
                        leituraProduto.clear()
                    elif barcodeData in leituraProduto and len(leituraEndereco) ==1 or len(leituraEndereco) >1:
                        leituraEndereco.clear()

                elif len(decode(imagem)) ==2:
                    if barcodeData in leituraProduto and len(leituraEndereco) != 1 or len(leituraProduto) ==2:
                        leituraEndereco.clear()
                    elif barcodeData in leituraEndereco and len(leituraProduto) != 1 or len(leituraEndereco) ==2:
                        leituraProduto.clear()
                
                if len(leituraEndereco) + len(leituraProduto) == len(decode(imagem)):
                    if len(leituraEndereco) == 1 and len(leituraProduto) ==0:
                        print('aguardando Produto')
                        cv2.rectangle(imagem, (x, y), (x + w, y + h), (255,0,0), 25)
                        leituraEndereco.clear()
                    elif len(leituraProduto) ==1 and len(leituraEndereco) ==0:
                        print('aguardando Endereco')
                        leituraProduto.clear()
                    elif len(leituraEndereco) >1:
                        print('mais de 1 endereco encontrado!',leituraEndereco) 

                    elif len(leituraProduto) >1:
                        print('mais de 1 produto encontrado',leituraProduto)       

                    else:
                        if len(leituraEndereco) + len(leituraProduto) == len(decode(imagem)):
                            valor = (leituraEndereco,leituraProduto)
                            return valor 
            else:
                cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 25)
        except:
            cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 25)

if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        height, width, channels = frame.shape
        result = lerqr(frame,height,width)
        
        if result and len(result) == 2:
            produto = (result[1][0])
            endereco = (result[0][0])
            valor = (endereco,produto)
            if endereco:

                conn = engine.connect()
                s = select(projetoEstoque.c.status).where(projetoEstoque.c.endereco == endereco)
                result1 = conn.execute(s)
                teste = result1.all()
                
                if teste != []:
                    if teste[0][0] == 1 and valor not in validado:
                        validado.append(valor)
                    else:
                        print('testre')
                else:
                    print('Nao encontrado !')


        for leitura in decode(frame):
                    (x, y, w, h) = leitura.rect
                    barcodeData = leitura.data.decode("utf-8")
                    for i in validado:
                        for o in i:
                            if o == barcodeData:
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 25)



        cv2.imshow("camera",frame)
        cv2.waitKey(5)