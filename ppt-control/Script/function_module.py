import cv2
import numpy as np
import time
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui


class HandGestureRecognizer():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            mode, maxHands, modelC, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def initialize(self, img):
        pass

    def findPosition(self, img, handNo=0):
        self.lmList = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(myHand.landmark):
                h, w, z = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)
        return img


class PoseGestureRecognizer():
    def __init__(self, model_complexity=1, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(model_complexity, smooth_landmarks, enable_segmentation,
                                     smooth_segmentation, min_detection_confidence, min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.volumeThreshold = 0.2
        self.scale = 30

    def initialize(self, img):
        self.crossThreshold = 1
        self.verticalThreshold = 1
        try:
            self.lmList = self.pose.process(cv2.cvtColor(
                img, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            self.crossThreshold = np.abs(
                (self.lmList[12].x - self.lmList[11].x)/(self.lmList[12].y - self.lmList[24].y))
            self.verticalThreshold = np.abs(
                (self.lmList[8].y - self.lmList[12].y)/(self.lmList[12].x - self.lmList[11].x))
            print(self.crossThreshold)
            print(self.verticalThreshold)
        except:
            pass

    def findPosition(self, img) -> None:
        self.lmList = []
        imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRBG)
        if self.results.pose_landmarks:
            self.mpDraw.draw_landmarks(
                img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, z = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)

        return img

    def volumeControl(self, imgPrev, imgCurr):
        try:
            self.lmList = self.pose.process(cv2.cvtColor(
                imgPrev, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            if self.lmList:
                if (self.lmList[15].visibility > 0.5 and self.lmList[16].visibility > 0.5):
                    if (np.abs((np.abs(float((self.lmList[15].x-self.lmList[16].x))))) < self.volumeThreshold):
                        self.curr = self.volume.GetMasterVolumeLevel()
                        self.prev_diff = (
                            np.abs(float((self.lmList[15].y-self.lmList[16].y))))
                        self.lmList = self.pose.process(cv2.cvtColor(
                            imgCurr, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
                        self.curr_diff = (
                            np.abs(float((self.lmList[15].y-self.lmList[16].y))))
                        self.curr += (float(self.curr_diff) -
                                      float(self.prev_diff))*self.scale
                        if (self.curr > -65.0 and self.curr < 0.0):
                            self.volume.SetMasterVolumeLevel(self.curr, None)
                        else:
                            pass
        except:
            pass

    def get_ratio_shoulder_height(self, img):
        try:
            newlmList = self.pose.process(cv2.cvtColor(
                img, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            shoulder = np.abs(newlmList[12].x - newlmList[11].x)
            height = np.abs(newlmList[0].y - newlmList[24].y)
            ratio = shoulder/height
            return ratio
        except:
            pass
        return None

    def get_shoulder_to_ear(self, img):
        try:
            newlmList = self.pose.process(cv2.cvtColor(
                img, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            dist = np.abs(newlmList[12].y - newlmList[8].x)
            return dist
        except:
            pass
        return None

    def activate(self, img):
        try:
            self.lmList = self.pose.process(cv2.cvtColor(
                img, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            if self.lmList:
                if ((self.lmList[15].x  - self.lmList[16].x) * (self.lmList[13].x - self.lmList[14].x) < 0):
                    if (self.lmList[15].y < self.lmList[11].y and self.lmList[16].y < self.lmList[12].y):
                        return True
                    else:
                        return False
            return False
        except:
            pass

    def slideControl(self, imgPrev, imgCurr):
        try:
            self.lmListPrev = self.pose.process(cv2.cvtColor(
                imgPrev, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark
            self.lmListCurr = self.pose.process(cv2.cvtColor(
                imgCurr, cv2.COLOR_BGR2RGB)).pose_landmarks.landmark

            if self.lmListPrev and self.lmListCurr:
                if (self.lmListPrev[15]).x > (self.lmListPrev[9]).x and (self.lmListCurr[15]).x < (self.lmListCurr[9]).x:
                    if np.abs((self.lmListPrev[12].x - self.lmListPrev[11].x)/(self.lmListPrev[12].y - self.lmListPrev[24].y)) > self.crossThreshold/1.5:
                    #     if (self.lmListPrev[15]).y < (self.lmListPrev[11]).y + self.get_shoulder_to_ear(imgCurr) and ((self.lmListCurr[15]).y > (self.lmListCurr[7]).y - self.get_shoulder_to_ear(imgCurr)/1.41):
                        if ((self.lmListPrev[15]).y < ((self.lmListPrev[23]).y+(self.lmListPrev[11]).y)/2) and ((self.lmListPrev[15]).y > (self.lmListPrev[1]).y):
                            pyautogui.press('right')
                            print('right')
                            
                            time.sleep(0.5)

                elif (self.lmListPrev[16]).x < (self.lmListPrev[10]).x and (self.lmListCurr[16]).x > (self.lmListCurr[10]).x:
                    if np.abs((self.lmListPrev[12].x - self.lmListPrev[11].x)/(self.lmListPrev[12].y - self.lmListPrev[24].y)) > self.crossThreshold/1.5:
                    #     if (self.lmListPrev[16]).y < (self.lmListPrev[12]).y + self.get_shoulder_to_ear(imgCurr) and ((self.lmListCurr[16]).y > (self.lmListCurr[8]).y - self.get_shoulder_to_ear(imgCurr)/1.41):
                        if (self.lmListPrev[16]).y < ((self.lmListPrev[24]).y+(self.lmListPrev[12]).y)/2 and ((self.lmListPrev[16]).y > (self.lmListPrev[4]).y):
                            pyautogui.press('left')
                            print('left')
                            time.sleep(0.5)
        except:
            pass
        return None


def main() -> None:
    '''
    The main function
    '''
    print("Library module for PPT control")
    return None


if __name__ == "__main__":
    main()
