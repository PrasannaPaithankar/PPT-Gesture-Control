import os
import cv2
from threading import Thread
import tkinter as tk
from tkinter import ttk
import function_module as fm


class GUI(tk.Frame):
    '''
    The GUI class
    Creates widgets and handles events
    '''

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.pack()
        # object of HandGestureRecognizer class
        # self.handRecognizer = fm.HandGestureRecognizer()
        # object of PoseGestureRecognizer class
        self.poseRecognizer = fm.PoseGestureRecognizer()
        # initializes GUI widgets
        self.create_widgets()

    def stream_window(self):
        # if url_inp is empty, use webcam
        if (self.url_inp.get() == ""):
            cap = cv2.VideoCapture(0)
            # cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        # else use the stream from IP Webcam
        else:
            cap = cv2.VideoCapture("http://"+self.url_inp.get()+"/video")

        # read the first frame
        framePrev = cv2.flip(cap.read()[1], 1)
        while True:
            # read the frame
            ret, frame = cap.read()
            if ret:
                # flip the frame
                frame = cv2.flip(frame, 1)
                # frame = self.poseRecognizer.findPosition(frame)
                # self.poseRecognizer.slideControl(framePrev, frame)
                # self.poseRecognizer.volumeControl(framePrev, frame)
                # self.handRecognizer.gestureControl()

                # initiate a thread for slide control
                # tslideControl = Thread(target=self.poseRecognizer.slideControl,
                #                        args=(framePrev, frame))
                # tslideControl.start()

                # initiate a thread for volume control
                # tvolumeControl = Thread(target=self.poseRecognizer.volumeControl,
                #                         args=(framePrev, frame))
                # tvolumeControl.start()

                # join the threads
                # tslideControl.join()
                # tvolumeControl.join()
                
                # if (self.poseRecognizer.activate(frame)):
                self.poseRecognizer.slideControl(framePrev, frame)

                # display the frame
                cv2.imshow('Frame', frame)
                framePrev = frame

            # press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # release the streaming device
        cap.release()
        cv2.destroyAllWindows()
        return None

    def initialize(self):
        cap = cv2.VideoCapture(0)
        frame = cv2.flip(cap.read()[1], 1)
        # self.handRecognizer.initialize(frame)
        self.poseRecognizer.initialize(frame)
        return None

    def openGitHub(self):
        import webbrowser
        webbrowser.open(
            'https://github.com/PrasannaPaithankar/PPT-Gesture-Control', new=2)
        return

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self.master)
        self.run = ttk.Frame(self.tabControl)
        self.settings = ttk.Frame(self.tabControl)
        self.about = ttk.Frame(self.tabControl)
        self.tabControl.add(self.run, text='Run')
        self.tabControl.add(self.settings, text='Settings')
        self.tabControl.add(self.about, text='About')
        self.tabControl.grid(row=0, column=0, padx=5, pady=10)

        self.url_inp_label = tk.Label(self.run, text="Enter stream URL:")
        self.url_inp_label.grid(row=1, column=0, padx=10, pady=10)
        self.url_inp = tk.Entry(self.run)
        self.url_inp.grid(row=1, column=1, padx=10, pady=10)

        self.stream_button = tk.Button(
            self.run, text="Stream", command=lambda: self.stream_window())
        self.stream_button.grid(row=2, column=0, padx=5, pady=10)

        self.initialize_button = tk.Button(
            self.run, text="Initialize", command=lambda: self.initialize())
        self.initialize_button.grid(row=2, column=1, padx=5, pady=10)

        self.about_label = tk.Label(
            self.about, text="Developed by: Technology Robotix Society\nVersion: 1.1.0 (2023)\nGPL-3.0 License", justify="left")
        self.about_label.grid(row=0, column=0, padx=5, pady=10)
        self.licenseFile = tk.Button(self.about, text="License",
                                width=15, command=lambda: os.startfile("LICENSE"))
        self.licenseFile.grid(row=1, column=0, padx=5, pady=10)
        self.githubLink = tk.Button(self.about, text="GitHub", width=15,
                               command=lambda: self.openGitHub())
        self.githubLink.grid(row=1, column=1, padx=5, pady=10)

        return None

    def stop(self):
        self.status = 0
        return None


if __name__ == "__main__":
    '''
    The main function
    Opens the tkinter GUI
    '''
    root = tk.Tk()
    root.title("PPT Gesture Control")
    app = GUI(master=root)
    app.mainloop()
