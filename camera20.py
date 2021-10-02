import cv2
from pyzbar.pyzbar import decode
import json
import numpy

webcam = cv2.VideoCapture(0)


    
produtos = []
endereco = []
# def lerqr(x):

#     for barcode in decode(x):
#         (x, y, w, h) = barcode.rect
#         barcodeData = barcode.data.decode("utf-8")
#         barcodeType = barcode.type

#         qr = json.loads(barcodeData)
#         try:
            
#             if (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) == 0:
#                 e = (qr['e'],x,y)
#                 endereco.append(e)
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1,1,2))
#                 cv2.polylines(frame,[pts],True,(255,0,255),5) 
#                 # text = "endereco ({})".format(e)
#             elif (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) > 0:
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1,1,2))
#                 cv2.polylines(frame,[pts],True,(255,0,255),5) 
                
                
        
#             if (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco != []:

#                 print((x / endereco[0][1]) > 0.5)
#                 print(x,endereco[0][1])
#                 e = ((qr['p'],qr['e']),x,y)
#                 produtos.append(e)
#                 print(produtos,qr,'x:',x,'y:',y)
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1,1,2))
#                 cv2.polylines(frame,[pts],True,(255,0,255),5) 
#             elif (qr['p'],qr['e'])  not in produtos and qr['p'] > 0 and len(produtos) > 0:
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1,1,2))
#                 cv2.polylines(frame,[pts],True,(255,0,255),5) 
#         except:
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1,1,2))
#                 cv2.polylines(frame,[pts],True,(0,0,255),50) 

def lerqr(x,height,width):
    start_point = (int(width / 4), int(height  / 4))
    end_point = (int(width / 1.35), int(height / 1.35))
    color = (255, 0, 0)
    thickness = 2
    cv2.rectangle(frame, start_point, end_point, color, thickness)

    for barcode in decode(x):
        (x, y, w, h) = barcode.rect
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        try:
            qr = json.loads(barcodeData)    

            if x < int(width / 1.35) and x > int(width / 4) and y < int(height / 1.35) and y > int(height / 4) and (qr['e']) not in endereco and qr['p'] == 0 and len(endereco) == 0:
                e = ((qr['e']),(x,y))
                endereco.append(e)
                
            elif x < int(width / 1.35) and x > int(width / 4) and y < int(height / 1.35) and y > int(height / 4) and (qr['p'],qr['e']) not in produtos and qr['p'] > 0 and len(produtos) == 0 and endereco !=[]:
                p = ((qr['p'],qr['e']),(x,y))
                produtos.append(p)
            
            
            if x < int(width / 1.35) and x > int(width / 4) and y < int(height / 1.35) and y > int(height / 4)and (qr['e']) and qr['p'] == 0 and qr['e'] == endereco[0][0] :
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

            
            if x < int(width / 1.35) and x > int(width / 4) and qr['p'] > 0 and (qr['p'],qr['e']) == produtos[0][0]:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


        except:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)



if webcam.isOpened():
    validacao, frame = webcam.read()
    while validacao:
        validacao, frame = webcam.read()
        height, width, channels = frame.shape
        lerqr(frame,height,width)
            

        cv2.imshow("camera",frame)
        cv2.waitKey(5)
    
    

            
