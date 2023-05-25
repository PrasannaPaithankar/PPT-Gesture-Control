from function_module import *
import mss
import cv2
import numpy as np

sct=mss.mss()

def main()->None:
    '''
    The main function
    '''
    monitor={"top":0, "left":960, "width":953, "height":1700} #The part of the screen to be captured
    while True:
        img=np.array(sct.grab(monitor)) #img contains the screenshot
        #To display the screen that is being recorded
        '''cv2.imshow("Screenshot", img)
        k=cv2.waitKey(1)
        if (k==ord("q")):
            break
    cv2.destroyAllWindows'''
    # analyze frames and execute actions
    return None

if __name__ == "__main__":
    main()
