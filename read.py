import cv2
import pymongo  
import tkinter as tk
from datetime import *
from bson.objectid import ObjectId
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['eventwk']
absent = mydb['absent']
event=mydb['event']
siswaa   = mydb['siswa']


# win = tk.Tk()


cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    _, img= cap.read()
    data, bbox, _= detector.detectAndDecode(img)
    if bbox is not None:
        for i in range(len(bbox)):
            point1 = tuple(bbox[i][0])
            point2 = tuple(bbox[(i+1)%len(bbox)][0])
            cv2.line(img, point1, point2, color=(225,0,0), thickness=2)
        if data:
            eid = event.find_one({'date':str(date.today())})
            fus = siswaa.count({'nis':int(data)})
            find = absent.count({'eventId':ObjectId(eid['_id']),'nis':int(data)})
            fd = event.count({'date':str(date.today())})
            if fus > 0:
                if fd > 0:
                    if find > 0:
                        print('You Have Absent !!!',data)
                        print('Event Found!!')
                    else:
                        rec = event.find_one({'date':str(date.today())})
                        recs = siswaa.find_one({'nis':int(data)})
                        x = absent.insert_one({'eventId':rec['_id'],'nis':int(data),'name':recs['fullname'],'rombel':recs['rombel'],'rayon':recs['rayon'],'createdAt':str(date.today())})
                        print('[+] QR Code Detected, data:', data)
                        print('Event Found!!')
                else:
                    print('Event not Found')
            else:
                print('Username Not Found!!')
    cv2.imshow('img',img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
# win.mainloop()