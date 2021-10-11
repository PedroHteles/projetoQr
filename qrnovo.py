import cv2
from pyzbar.pyzbar import decode
import json
import numpy as np

leituraProduto = []
leituraEndereco = []


def lerqr(x):
    for barcode in decode(x):
        barcodeData = barcode.data.decode("utf-8")
        if len(barcodeData) == 16:
            if barcodeData not in leituraProduto:
                leituraProduto.append(barcodeData)
                # modulo = leituraProduto[0:2]
                # rua = leituraProduto[2:6]
                # predio = leituraProduto[6:9]
                # endereco = leituraProduto[9:12]
                # produto = leituraProduto[12:]
            pass
        elif  len(barcodeData) == 12:
            if barcodeData not in leituraEndereco:
                leituraEndereco.append(barcodeData)
                # modulo = leituraEndereco[0:2]
                # rua = leituraEndereco[2:6]
                # predio = leituraEndereco[6:9]
                # endereco = leituraEndereco[9:]

        if len(decode(x)) > 2:
            print(' mais de 2 qr encontrado')
            if len(leituraEndereco) + len(leituraProduto) == len(decode(img)):
                valor = (leituraEndereco,leituraProduto)
                return valor     
        else:
            pass
        if len(decode(x)) == 1:
            if barcodeData in leituraEndereco and len(leituraProduto) == 1:
                leituraProduto.clear()
            elif barcodeData in leituraProduto and len(leituraEndereco) == 1:
                leituraEndereco.clear()
            if len(leituraEndereco) > 1:
                leituraEndereco.clear()
            elif len(leituraProduto) >1:
                leituraProduto.clear()
        elif len(decode(img)) == 2:
            if barcodeData in leituraProduto and len(leituraEndereco) != 1:
                leituraEndereco.clear()
            elif barcodeData in leituraEndereco and len(leituraProduto) != 1:
                leituraProduto.clear()
            if barcodeData in leituraEndereco and len(leituraEndereco) == 2:
                leituraProduto.clear()
            elif barcodeData in leituraProduto and len(leituraProduto) == 2:
                leituraEndereco.clear()
        
        if len(leituraEndereco) + len(leituraProduto) == len(decode(img)):
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
                print(leituraEndereco,leituraProduto)
            



while True:
    img = cv2.imread('./img/image0.jpg')
    height, width, channels = img.shape
    lerqr(img)
  
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break