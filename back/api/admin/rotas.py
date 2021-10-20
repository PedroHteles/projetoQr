from api import engine
from api.admin.models import projetoEstoque
from sqlalchemy.sql import select
import cv2
import numpy as np
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)

endereco = []
produto = []

def lerqr(frame):

    for barcode in pyzbar.decode(frame):
        (x, y, w, h) = barcode.rect
        leituraArea = x < (end_point[0]-w) and x > start_point[0] and y < (end_point[1]-h) and y > start_point[1] 
        if leituraArea:
            barcodeData = barcode.data.decode("utf-8")
            if len(barcodeData) == 12:
                if barcodeData not in endereco:
                    endereco.append(barcodeData)
                pass
            elif len(barcodeData) == 16:
                if barcodeData not in produto:
                    produto.append(barcodeData)
                pass
            if len(endereco) >=1 and len(produto) >= 1:
                if((len(endereco) + len(produto) )% 2 == 0):
                    valor = [endereco,produto]
                    # print(endereco[-1],produto[-1])
                    return valor
while True:
    _, img = cap.read()
    height, width, channels = img.shape
    start_point = (int(width / 6), int(height  / 12))
    end_point = (int(width / 1.25), int(height / 1.05))
    cv2.rectangle(img, start_point, end_point,(255,0,0),2)

    result = lerqr(img)

    if result:
        resultados = (result[0],result[1])
        for barcode in pyzbar.decode(img):
            (x, y, w, h) = barcode.rect
            leituraArea = x < (end_point[0]-w) and x > start_point[0] and y < (end_point[1]-h) and y > start_point[1] 
            if leituraArea:
                barcodeData = barcode.data.decode("utf-8")
                if barcodeData in resultados[0]:
                    
                    qrEndereco = np.array(result[0])
                    a = np.where(qrEndereco == barcodeData)[0][0]
                    resultadoLeitura = [result[0][a],result[1][a]]
                    valorEndereco = resultadoLeitura[0]
                    valorProduto = resultadoLeitura[1]
       
                    if resultadoLeitura:
                        conn = engine.connect()
                        s = select(projetoEstoque.c.status).where(projetoEstoque.c.endereco == valorEndereco, projetoEstoque.c.produto == valorProduto)
                        result1 = conn.execute(s)
                        resultado = result1.all()
                        
                        if resultado != []:
                            if resultado[0][0] == 0:
                                teste = projetoEstoque.update().where(projetoEstoque.c.endereco == valorEndereco, projetoEstoque.c.produto == valorProduto).values(status=1)
                                conn.execute(teste)
                            else:
                                print('validado') 
                        else:
                            print('Nao encontrado !')
                            s = select(projetoEstoque.c.produto).where(projetoEstoque.c.endereco == valorEndereco)
                            result1 = conn.execute(s)
                            resultado = result1.one()[0]
                            if resultado != produto:
                                print('Endereco errado',resultado,produto)
                            else:
                                print('ERRO!')

    cv2.imshow("QRCODEscanner", img)    
    # cv2.imshow("camera",img)
    key = cv2.waitKey(5)
