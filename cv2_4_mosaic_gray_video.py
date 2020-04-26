import sys, traceback
import numpy as np
import cv2 as cv

ratio = 0.05

def main():
    try:
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
            
            # make mozaic
            imageSmall = cv.resize(frame_gray, None, fx=ratio, fy=ratio, interpolation=cv.INTER_NEAREST)
            imageMosaic = cv.resize(imageSmall, frame_gray.shape[:2][::-1], interpolation=cv.INTER_NEAREST)

            # Display the resulting frame
            cv.imshow('imageSmall', imageMosaic)

            k = cv.waitKey(1)
            if k == 27: # wait for ESC key to exit
                cv.destroyAllWindows()
            elif k == ord('s'): # wait for 's' key to save and exit
                cv.imwrite('mosaic_'+args[1],imageMosaic)
                cv.destroyAllWindows()

        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()

    except:
        print("error")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
