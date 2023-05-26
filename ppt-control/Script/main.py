from function_module import *
import tkinter as tk
import cv2

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
    
    while True:
        ret,frame=vid.read()
        if not ret:
            continue
        cv2.imshow("Video", video)
        k=cv2.waitKey(1)
        if (k==ord("q")):
            break
    
    # analyze frames and execute actions
    return None

if __name__ == "__main__":
    main()
