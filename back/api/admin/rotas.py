from re import escape
from api import engine
from api.admin.models import projetoEstoque
from sqlalchemy.sql import select
import cv2
from pyzbar.pyzbar import decode
import simplejson as json


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
                
                if len(barcodeData) ==16 and leituraEndereco !=[] and barcodeData not in leituraProduto:
                    leituraProduto.append(barcodeData)
                elif  len(barcodeData) ==12 and barcodeData not in leituraEndereco:
                    leituraEndereco.append(barcodeData)

                # if len(leituraEndereco) + len(leituraProduto) == len(decode(imagem)) and len(decode(imagem)) >2:
                #     print(' mais de 2 qr encontrado')
                #     valor = (leituraEndereco,leituraProduto)
                #     return valor
                # elif len(decode(imagem)) ==1:
                #     if barcodeData in leituraEndereco and len(leituraProduto) ==1 or len(leituraProduto) >1:
                #         leituraProduto.clear()
                #     elif barcodeData in leituraProduto and len(leituraEndereco) ==1 or len(leituraEndereco) >1:
                #         leituraEndereco.clear()

                # elif len(decode(imagem)) ==2:
                #     if barcodeData in leituraProduto and len(leituraEndereco) != 1 or len(leituraProduto) ==2:
                #         leituraEndereco.clear()
                #     elif barcodeData in leituraEndereco and len(leituraProduto) != 1 or len(leituraEndereco) ==2:
                #         leituraProduto.clear()
                
                if len(leituraEndereco) + len(leituraProduto) == len(decode(imagem)):
                    if len(leituraEndereco) == 1 and len(leituraProduto) ==0:
                        print('aguardando Produto')
                        cv2.rectangle(imagem, (x, y), (x + w, y + h), (255,0,0), 25)
                        # leituraEndereco.clear()
                    elif len(leituraProduto) ==1 and len(leituraEndereco) ==0:
                        print('aguardando Endereco')
                        # leituraProduto.clear()
                    elif len(leituraEndereco) >1:
                        print('mais de 1 endereco encontrado!',leituraEndereco) 
                    elif len(leituraProduto) >1:
                        print('mais de 1 produto encontrado',leituraProduto)       
                    else:
                        if len(leituraEndereco) + len(leituraProduto) == len(decode(imagem)):
                            valor = (leituraEndereco,leituraProduto)
                            return valor 
            else:
                cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 5)
        except:
            cv2.rectangle(imagem, (x, y), (x + w, y + h), (0,0,255), 5)

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
            if endereco and produto:
                conn = engine.connect()
                s = select(projetoEstoque.c.status).where(projetoEstoque.c.endereco == endereco, projetoEstoque.c.produto == produto)
                result1 = conn.execute(s)
                resultado = result1.all()
                
                if resultado != []:
                    if resultado[0][0] == 0:
                        teste = projetoEstoque.update().where(projetoEstoque.c.endereco == endereco, projetoEstoque.c.produto == produto).values(status=1)
                        conn.execute(teste)
                    else:
                        print('validado') 
                        for leitura in decode(frame):
                            (x, y, w, h) = leitura.rect
                            barcodeData = leitura.data.decode("utf-8")
                            for i in valor: 
                                if i == barcodeData:
                                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 5)
                else:
                    print('Nao encontrado !')
                    s = select(projetoEstoque.c.produto).where(projetoEstoque.c.endereco == endereco)
                    result1 = conn.execute(s)
                    resultado = result1.one()[0]
                    if resultado != produto:
                        print('Endereco errado',resultado,produto)
                    else:
                        print('ERRO!')



        cv2.imshow("camera",frame)
        cv2.waitKey(5)