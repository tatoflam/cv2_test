import sys, traceback
import numpy as np
import cv2 as cv

def main():
    args = sys.argv
    print(args)
    print(args[0])
    print(args[1])
    print(str(len(args)))
    if not len(args) == 2:
        print(args[0])
        print(args[1])
        print("please enter 1 parameter of image file name")
        exit(1)

    try:
        src = cv.imread(args[1])
        if not src is None:
            print('Image is read.')
        else:
            print('Image is not read.')
            exit(1)
        
        cv.imshow('image',src)
        k = cv.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv.destroyAllWindows()
        elif k == ord('s'): # wait for 's' key to save and exit
            cv.imwrite('mosaic_'+args[1],imageSmall)
            cv.destroyAllWindows()


        height = src.shape[0]
        width = src.shape[1]
        print("src: " ,src)
        print("src.shape: " ,src.shape)
        print("src.shape[0] :" ,src.shape[0])
        print("src.shape[1] :" ,src.shape[1])
        print("src.shape[:2][::-1] :" ,src.shape[:2][::-1])

        ratio=0.05
        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        imageSmall = cv.resize(src_gray, None, fx=ratio, fy=ratio, interpolation=cv.INTER_NEAREST)
        imageMosaic = cv.resize(imageSmall, src.shape[:2][::-1], interpolation=cv.INTER_NEAREST)
        cv.imshow('imageSmall', imageMosaic)
        k = cv.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv.destroyAllWindows()
        elif k == ord('s'): # wait for 's' key to save and exit
            cv.imwrite('mosaic_'+args[1],imageSmall)
            cv.destroyAllWindows()

    except:
        print("error")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
