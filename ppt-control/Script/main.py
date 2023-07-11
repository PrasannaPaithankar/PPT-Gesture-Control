from function_module import *
import tkinter as tk
import cv2
import mediapipe as mp
import cv2
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math


class pose():
    def __init__(self):
        self.mp_draw=mp.solutions.drawing_utils
        self.draw_styles=mp.solutions.drawing_styles
        self.poses=mp.solutions.pose.Pose(model_complexity=0)
        self.threshold=0.2
        self.scale=100
        self.state=0

    def wrist_coord(self, img)->None:
        '''
        This function takes an image (frame) as an input and returns the coordinates of both the wrists. 
        '''
        self.img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.poses.process(self.img1)
        self.lm=self.result.pose_landmarks
        if self.lm:
            self.x1=self.lm.landmark[15].x
            self.y1=self.lm.landmark[15].y
            self.z1=self.lm.landmark[15].z
            self.x2=self.lm.landmark[16].x
            self.y2=self.lm.landmark[16].y
            self.z2=self.lm.landmark[16].z
            
    def draw(self, img)->None:
        '''
        This function is to draw the landmarks on the frame to visualize the landmarks.
        '''
        self.mp_draw.draw_landmarks(
            img,
            self.lm,
            mp.solutions.pose.POSE_CONNECTIONS,
            self.draw_styles.get_default_pose_landmarks_style()
        )

class VolumeControl(pose):
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        super().__init__()
        
    def recognizeStart(self)->None:
        '''
        This method recognizes the start of the Gesture that is used to control the volume.
        In our case it is to bring both the hands together.
        '''
        if (self.result.pose_landmarks):
            if (self.lm.landmark[15].visibility>0.5 and self.lm.landmark[16].visibility>0.5):
                if (math.fabs(self.x1-self.x2)<self.threshold and math.fabs(self.z1-self.z2)<self.threshold):
                    self.curr_y=self.y1
                    self.state=1
                else:
                    self.state=0
                    
    def recognizeGesture(self)->None:
        '''
        This method is to recignize the gesture.
        In our case it is to increase the gap between the hands by moving one of the hands while keeping the other in the same position.
        '''
        if self.lm:
            if (self.lm.landmark[15].visibility>0.5 and self.lm.landmark[16].visibility>0.5):
                if (math.fabs(self.x1-self.x2)<self.threshold and math.fabs(self.z1-self.z2)<self.threshold):
                    self.curr=self.volume.GetMasterVolumeLevel()
                    self.prev_y=self.curr_y
                    self.curr_y=self.y1
                    self.curr+=(self.prev_y-self.curr_y)*self.scale
                    if (self.curr>-65.0 and self.curr<0.0):
                        self.volume.SetMasterVolumeLevel(self.curr, None)
                        self.state=1
                    else:
                        pass
                else:
                    self.state=0

class GUI:
    def __init__(self):
        self.root=tk.Tk()

        self.frame=tk.Frame(self.root)
        self.frame.pack()

        self.label=tk.Label(self.frame, text="Enter the URL")
        self.label.pack()

        self.txtbox=tk.Text(self.root,height=1)
        self.txtbox.pack(padx=10,pady=10)

        self.button=tk.Button(self.root, text="Enter", width=10, command=self.Enter)
        self.button.pack(pady=10)

        self.root.mainloop()
    def Enter(self):
    '''
        This will store the text entered in the textbox of tkinter interface and close the interface when the enter button is pressed
    '''
        self.string=self.txtbox.get("1.0", tk.END)  
        if (len(self.string)!=1):
            self.root.destroy()
     
def main()->None:
    '''
    The main function
    '''
    tkinter_object=GUI()
    vid=cv2.VideoCapture(tkinter_object.string+"/video")
    poserec=VolumeControl()
    
    while True:
        ret,frame=vid.read()
        if not ret:
            continue
            
        poserec.wrist_coord(frame)
        poserec.draw(frame)
        
        if (poserec.state==0):
            poserec.recognizeStart()
        elif (poserec.state==1):
            poserec.recognizeGesture()
            
        cv2.imshow("Video", cv2.flip(frame,1))
        
        k=cv2.waitKey(1)
        if (k==ord("q")):
            break
            
    cv2.destroyAllWindows()
    
    return None

if __name__ == "__main__":
    main()
