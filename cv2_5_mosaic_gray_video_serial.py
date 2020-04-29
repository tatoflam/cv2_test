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
            print("Cannot open camera\n")
            exit(1)
        
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...\n")
                break
            
            # Convert to gray scale
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # print("accessing to serial_q")
            item = serial_q.get()
            print("video_stream: get_from_serial_q: %s" % item)
            # check stop order from receiver
            if item is "Stop":
                break
            elif item is None:
                item = prev_item
            # if receiver is working and no object in queue, use previous item
            else:
                prev_item = item
            
            print("video_stream item: %s" % item)
            

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

    print("receiver started\n")
    while not quit_recv:
        
        data =  s.readline()
        
        # this did not work - print from concurrent thread block the process
        # print("serial received(%s)" % data.encode("utf-8")) .. this did not work
        print("receiver: serial received: %s" % data)
        # sys.stdout.write("\rserial received(%s)\n" % data)
        # sys.stdout.flush()
        serial_q.put(data)
        # time.sleep(0.5)
    serial_q.put("Stop")
    print("receiver stopped\n")



def init_serial():

    status, outputs = getstatusoutput("ls -1 /dev/ttyUSB*")
    for output in outputs.split('\n'):
        try: 
            port = output
            baudrate=115200
            s = serial.Serial(port=port, baudrate=baudrate)
            print("Serial is opened over %s in %i bps\n" % (port, baudrate))
            return s
        except:
            print(traceback.format_exc())
            print("No device found\n")
        

def main():        
    global serial_q
    global quit_recv

    try:
        s = init_serial()
        if (s == None):
            print("Serial port cannot be opened\n")
            exit(1)

        # start serial as a concurrent executor
        quit_recv = False
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        receiver = executor.submit(recv_serial, s)

        # start video stream
        video_stream()

        while True:
            try:
                key = input()
                time.sleep(1) # wait for checking input
                if(key == "f"):
                    break
                    
                # if anything from standard input, write back to AVR.
                key += "\n"
                s.write(key)
            except:
                print(traceback.format_exc())
                print("\nstop receiver thread\n")
                exit(1)
        
    except concurrent.futures.CancelledError:
        print(traceback.format_exc())
        print("executor is cancelled\n")
    except:
        print(traceback.format_exc())
    finally:
        print("main is waiting")
        # do not wait the queue empty as AVR is working asynchronouly
        # serial_q.join()
        
        quit_recv = True
        # wait until executor(receiver) finishes
        while not receiver.done():
            time.sleep(1)
        s.close

        print("main finished")
        exit(0)

if __name__ == "__main__":
    main()
 
