from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import imageTest_pb2
import imageTest_pb2_grpc


_ONE_DAY_IN_SECONDS = 0


class Greeter(imageTest_pb2_grpc.ImageTestServicer):

  def Analyse(self, request_iterator, context):
    cnt=1
    i=0
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    ppl_counter = None
    ttt=0
    flag = 1   #  -1 is skip. 1 is dont skip
    for req in request_iterator:
        time.process_time()
        print('time diff= '+str( time.process_time() - ttt) )
        ttt = time.process_time()
        
        frame = np.array(list(req.img))
        frame = frame.reshape( (1080,1920) )
        frame = np.array(frame, dtype = np.uint8 )

        meow = 5
        # if ppl_counter is None:
        #     ppl_counter = PeopleCounter(frame.shape[:2], DIVIDER1)
    
        #This line will currently not work as the people counting code is not there. Replace this line with whatever processing you want to do
        #do on the streamed video. 'processed' is the frame of the resulting video after processing.
        processed = frame
    
        #display processed video
        cv2.imshow('Processed Image', processed)
        cv2.waitKey(1)
        
        # ppl_counter.people_count1 is the current count of people. Replace it with whatever value you want to continuosly send back to the client
        #This line will send a value back to the client for each frame.
        yield imageTest_pb2.MsgReply(reply=meow )



def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  imageTest_pb2_grpc.add_ImageTestServicer_to_server(Greeter(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
