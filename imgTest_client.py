from __future__ import print_function

import grpc
import cv2
import imageTest_pb2
import imageTest_pb2_grpc
import skvideo.io

# URL = "/home/tt/Videos/VID_20201202_133703_090.mp4"
URL = "rtsp://admin:Aa123456@192.168.1.3:554/onvif1"

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = imageTest_pb2_grpc.ImageTestStub(channel)
  #temp = cv2.imread('/home/nirvan/img_one.png')
  for response in stub.Analyse( generateRequests() ):
      print(str(response.reply))




def generateRequests():
    videogen = skvideo.io.vreader(URL)
    i=0
    cnt = 1
    for frame in videogen:
        
        if(cnt == 5):
            cnt = 1
        else:
            cnt+=1
            continue
        
        frame = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
        frame = bytes(frame)
        yield imageTest_pb2.MsgRequest(img= frame)
    

if __name__ == '__main__':
  run()
