import cv2
from pyzbar.pyzbar import decode
import numpy as np

leituraProduto = []
leituraEndereco = []

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
                if len(barcodeData) ==16:
                    if barcodeData not in leituraProduto:
                        leituraProduto.append(barcodeData)
                    pass
                elif  len(barcodeData) ==12:
                    if barcodeData not in leituraEndereco:
                        leituraEndereco.append(barcodeData)
                    pass
                else:
                    cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 15)

                if len(leituraEndereco) + len(leituraProduto) == len(decode(img)) and len(decode(imagem)) >2:
                    print(' mais de 2 qr encontrado')
                    valor = (leituraEndereco,leituraProduto)
                    return valor
                elif len(decode(imagem)) ==1:
                    if barcodeData in leituraEndereco and len(leituraProduto) ==1 or len(leituraProduto) >1:
                        leituraProduto.clear()
                    elif barcodeData in leituraProduto and len(leituraEndereco) ==1 or len(leituraEndereco) >1:
                        leituraEndereco.clear()

                elif len(decode(imagem)) ==2:
                    if barcodeData in leituraProduto and len(leituraEndereco) !=1 or len(leituraProduto) ==2:
                        leituraEndereco.clear()
                    elif barcodeData in leituraEndereco and len(leituraProduto) !=1 or len(leituraEndereco) ==2:
                        leituraProduto.clear()
                
                if len(leituraEndereco) + len(leituraProduto) == len(decode(img)):
                    if len(leituraEndereco) ==1 and len(leituraProduto) ==0:
                        print('aguardando Produto')
                        leituraEndereco.clear()
                    elif len(leituraProduto) ==1 and len(leituraEndereco) ==0:
                        print('aguardando Endereco')
                        leituraProduto.clear()
                    elif len(leituraEndereco) >1:
                        print('mais de 1 endereco encontrado!',leituraEndereco) 
                    elif len(leituraProduto) >1:
                        print('mais de 1 produto encontrado',leituraProduto)        
                    else:
                        valor = (leituraEndereco,leituraProduto)
                        return valor 
            else:
                cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 25)
        except:
            cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 25)

while True:
    img = cv2.imread('./img/image0.jpg')
    height, width, channels = img.shape
    result = lerqr(img,height,width)
    # print(result)
    for leitura in decode(img):
        (x, y, w, h) = leitura.rect
        if result and len(result) == 2 :
            start_point = (int(width / 8), int(height  / 8))
            end_point = (int(width / 1.15), int(height / 1.15))
            leituraArea = x < (end_point[0] - w) and x > start_point[0] and y < (end_point[1] - h ) and y > start_point[1] 
            barcodeData = leitura.data.decode("utf-8")
            if leitura:
                for i in result:
                    if barcodeData == i[0]:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 15)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 15)
    # modulo = leituraProduto[0:2]
    # rua = leituraProduto[2:6]
    # predio = leituraProduto[6:9]
    # endereco = leituraProduto[9:12]
    # produto = leituraProduto[12:]
  
    cv2.imshow("camera",img)
    key = cv2.waitKey(5)
    if key == 27:
        break