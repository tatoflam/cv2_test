import sys, traceback
import serial
from subprocess import getstatusoutput  

import math
import numpy as np
import cv2 as cv
import time
import concurrent.futures
import queue

ratio = 0.05
serial_q = queue.Queue()
quit_recv = False
prev_item = None


def video_stream():
    try:
        global serial_q
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit(1)
        
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            # Convert to gray scale
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # print("accessing to serial_q")
            item = serial_q.get()
            print("get_from_serial_q: ", item)
            # check stop order
            if item is "Stop":
                break
            elif item is None:
                item = prev_item
            # if receiver is working and no object in queue, use previous item
            else:
                prev_item = item
            
            print("item: ", item)
            

#            ratio = math.floor(1/item, 3)
#            print("ratio: ", ratio)
            
            # make mozaic
            imageSmall = cv.resize(frame_gray, None, fx=ratio, fy=ratio, interpolation=cv.INTER_NEAREST)
            imageMosaic = cv.resize(imageSmall, frame_gray.shape[:2][::-1], interpolation=cv.INTER_NEAREST)

            # Display the resulting frame
            cv.imshow('imageSmall', imageMosaic)
            # print(np.ndarray(imageMosaic))
            k = cv.waitKey(1)
            if k == 27: # wait for ESC key to exit
                break
            
            elif k == ord('s'): # wait for 's' key to save and exit
                cv.imwrite('mosaic_'+args[1],imageMosaic)
                break
                

    except:
        print("error")
        print(traceback.format_exc())
    finally:
        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()

    

def recv_serial(s):
    global serial_q
    global quit_recv

    while not quit_recv:
        print("receiver started")

        data =  s.readline()
        # print("serial received(%s)" % data.encode("utf-8")) .. this did not work
        # print("serial received(%s)" % data)
        sys.stdout.write("\rserial received(%s)" % data)
        # sys.stdout.flush()
        serial_q.put(data)
        # time.sleep(0.5)
    serial_q.put("Stop")
    s.close



def init_serial():
    try:
        status, output = getstatusoutput("ls /dev/ttyUSB*")
        port = output
        baudrate=115200
        print("Port status: ", status)
        s = serial.Serial(port=port, baudrate=baudrate)
        print("Serial is opened over %s in %i bps" % (port, baudrate))
        return s
    except:
        print(traceback.format_exc())
        print("No device found")
        exit(1)
        

def main():
    s = init_serial()
    global serial_q
    global quit_recv

    try:

        # start serial as a concurrent executor
        quit_recv = False
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        receiver = executor.submit(recv_serial, s)

        # start video stream
        video_stream()

        while True:
            try:
                key = input().strip()
                time.sleep(0.1) # wait for checking input
                if(key ==""):
                    quit_recv = True
                    # wait until executor(receiver) finishes
                    while not receiver.done():
                        time.sleep(1)
                    print("stop main")
                    exit(0)
                    

                # if anything from standard input, write back to AVR.
                key += "\n"
                s.write(key)
            except:
                print(traceback.format_exc())
                print("\nstop receiver thread")
                exit(1)
        
    except concurrent.futures.CancelledError:
        print(traceback.format_exc())
        print("executor is cancelled")
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
 
