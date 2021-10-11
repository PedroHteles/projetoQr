import cv2
from pyzbar.pyzbar import decode
import json
import numpy

webcam = cv2.VideoCapture(0)


banco = ({'end': 0, 'e': 21}, {'p': 10, 'e': 21})
validado = []
naoValido = []

leituraProduto = []
leituraEndereco = []
area = []

def lerqr(x,height,width):
    start_point = (int(width / 8), int(height  / 8))
    end_point = (int(width / 1.15), int(height / 1.15))
    cv2.rectangle(frame, start_point, end_point,(255,0,0),2)
    
    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        leituraArea = x < (end_point[0] - w) and x > start_point[0] and y < (end_point[1] - h ) and y > start_point[1] 
        try:
            qr = json.loads(barcodeData)
            qrEnd = 'end' in qr
            qrProd = 'p' in qr
            if leituraArea:
                if qrEnd and qr not in leituraEndereco:
                    leituraEndereco.append(qr) 
                elif  qrProd and qr not in leituraProduto:
                    leituraProduto.append(qr)

                if len(decode(frame)) > 2:
                    print(' mais de 2 qr encontrado')
                    if len(leituraEndereco) + len(leituraProduto) == len(decode(frame)):
                        valor = (leituraEndereco,leituraProduto)
                        return valor     
                else:
                    pass
                if len(decode(frame)) == 1:
                    if qrEnd and len(leituraProduto) == 1:
                        leituraProduto.clear()
                    elif qrProd and len(leituraEndereco) == 1:
                        leituraEndereco.clear()
                    if len(leituraEndereco) > 1:
                        leituraEndereco.clear()
                    elif len(leituraProduto) >1:
                        leituraProduto.clear()
               
                elif len(decode(frame)) == 2:
                    if qrProd and len(leituraEndereco) != 1:
                        leituraEndereco.clear()
                    elif qrEnd and len(leituraProduto) != 1:
                        leituraProduto.clear()
                    if qrEnd and len(leituraEndereco) == 2:
                        leituraProduto.clear()
                    elif qrProd and len(leituraProduto) == 2:
                        leituraEndereco.clear()
     
                if len(leituraEndereco) + len(leituraProduto) == len(decode(frame)):
                    if len(leituraEndereco) == 1 and len(leituraProduto) == 0:
                        print('aguardando Produto')
                        leituraEndereco.clear()
                    elif len(leituraProduto) == 1 and len(leituraEndereco) == 0:
                        print('aguardando Endereco')
                        leituraProduto.clear()
                    elif len(leituraEndereco) > 1:
                        print('mais de 1 endereco encontrado!',leituraEndereco) 
                    elif len(leituraProduto) > 1:
                        print(' mais de 1 produto encontrado',leituraProduto)
                    else:
                        valor = (leituraEndereco,leituraProduto)
                        return valor  
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 15)                   
        except:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255, 255), 2)

if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        height, width, channels = frame.shape
        lerqr(frame,height,width)
            

        cv2.imshow("camera",frame)
        cv2.waitKey(5)
    
    

            
