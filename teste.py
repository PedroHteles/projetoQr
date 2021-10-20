import cv2
import numpy as np
from pyzbar import pyzbar


cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

endereco = []
produto = []

def lerqr(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
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
            if len(endereco) >=1 and  len(produto) >= 1 and len(pyzbar.decode(frame)) == 2 or  (len(pyzbar.decode(frame)) -2) < len(endereco) + len(produto) :
                if endereco !=[] and produto !=[] and len(pyzbar.decode(frame)) == 2 :
                    if((len(endereco) + len(produto) )% 2 == 0) :
                        valor = [endereco,produto]
                        return valor
while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    det = cv2.QRCodeDetector()
    height, width, channels = img.shape
    start_point = (int(width / 6), int(height  / 12))
    end_point = (int(width / 1.25), int(height / 1.05))
    cv2.rectangle(img, start_point, end_point,(255,0,0),2)

    # rv, pts = det.detectMulti(np.hstack([img, img])) 
    barcodees = pyzbar.decode(img)
    result = lerqr(img)
    if result:
        resultados = (result[0],result[1])
        for barcode in barcodees:
            (x, y, w, h) = barcode.rect
            leituraArea = x < (end_point[0]-w) and x > start_point[0] and y < (end_point[1]-h) and y > start_point[1] 
            if leituraArea:
                barcodeData = barcode.data.decode("utf-8")
                if barcodeData in resultados[0]:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 5)
                
                    qrEndereco = np.array(result[0])
                    a = np.where(qrEndereco == barcodeData)[0][0]
                    resultadoLeitura = [result[0][a],result[1][a]]
                    print(resultadoLeitura[0],resultadoLeitura[1])
       
    #     if resultadoLeitura:
    #         print(result,resultados)
                    # conn = engine.connect()
                    # s = select(projetoEstoque.c.status).where(projetoEstoque.c.endereco == resultadoLeitura[1], projetoEstoque.c.produto == resultadoLeitura[0])
                    # result1 = conn.execute(s)
                    # resultado = result1.all()
                    
                    # if resultado != []:
                    #     if resultado[0][0] == 0:
                    #         teste = projetoEstoque.update().where(projetoEstoque.c.endereco == resultadoLeitura[1], projetoEstoque.c.produto == resultadoLeitura[0]).values(status=1)
                    #         conn.execute(teste)
                    #     else:
                    #         print('validado') 
                    #         for leitura in decode(frame):
                    #             (x, y, w, h) = leitura.rect
                    #             barcodeData = leitura.data.decode("utf-8")
                    #             for i in valor: 
                    #                 if i == barcodeData:
                    #                     cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 5)
                    # else:
                    #     print('Nao encontrado !')
                    #     s = select(projetoEstoque.c.produto).where(projetoEstoque.c.endereco == resultadoLeitura[1])
                    #     result1 = conn.execute(s)
                    #     resultado = result1.one()[0]
                    #     if resultado != produto:
                    #         print('Endereco errado',resultado,produto)
                    #     else:
                    #         print('ERRO!')

    cv2.imshow("QRCODEscanner", img)    
    # cv2.imshow("camera",img)
    key = cv2.waitKey(5)
