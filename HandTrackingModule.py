###########################################################################
# This File is the base Hand detection module and needs to be imported in #
# all image processing py scripts and there we will create a instance of  #
# handsDetector class and use its functions                               #
###########################################################################

#### Imports ####
import cv2
import mediapipe as mp
import time
import numpy as np

#### Main class we will use in other py files ####
class HandsDetector():

    #### The init function with standard mediapipe variables ####
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.model1C = modelC

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model1C, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    #### Finds Hands and draws lines on them ####
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    #### Find the hand with given hand no and highlits it using blue circles ####
    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, z = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)

        return lmList

    #### The function to detect the direction the hand is pointing to ####
    def direction_hand(self, img, thres, ind_1, ind_2, flag):
        img = self.findHands(img)
        lmList = self.findPosition(img)
        if len(lmList) != 0:
            x = (lmList[ind_1][1] - lmList[ind_2][1])
            y = (lmList[ind_1][2] - lmList[ind_2][2])
            vec1 = np.array([lmList[4][1] - lmList[2][1], lmList[4][2] - lmList[2][2]])
            vec2 = np.array([lmList[8][1] - lmList[2][1], lmList[8][2] - lmList[2][2]])
            angle = np.arccos((np.dot(vec1, vec2))/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))

            # if y > thres:
            #     return 'd'

            # elif y < -thres:
            #     return 'u'

            # elif x > thres:
            #     return 'l'

            # elif x < -thres:
            #     return 'r'
            if angle > 1:
                return 'action'
            
            else:
                return 'dull'

        return flag

    #### The function to detect and return the hand no for left and right hand ####
    def left_or_right(self, img):
        img = self.findHands(img, draw=False)
        lmList = self.findPosition(img, draw=False)
        if len(lmList) != 0:
            num_hands = len(self.results.multi_handedness)
            # if num_hands != 2:
            #     # print(num_hands)
            #     # print("I got removed Here")
            #     return False, 2, 2
            for id, classification in enumerate(self.results.multi_handedness):
                # print("I got here !!!!!!!!!!")
                if classification.classification[id].label == "Left":
                    l = classification.classification[id].index
                    return 'lh'
                elif classification.classification[id].label == "Right":
                    r = classification.classification[id].index
                    return 'rh'
                else:
                    print("What the hell just happened....heh?")
                    return False, 2, 2
        return False, 2, 2
        
    # #### The function to detect whether a finger is open or closed ####
    # # tip_num => 8, 12, 16, 20
    # def num_fingers(self, img, hand_flag, tip_num):

    #     flag, left, right = self.left_or_right(img)
    #     if flag:
    #         if hand_flag == "l":
    #             hand_index = left
    #         elif hand_flag == "r":
    #             hand_index = right
    #         else:
    #             print("Please check the hand_flag Parameter")
    #             return False
    #         lmList = self.findPosition(img, draw=False, handNo=hand_index)

    #         if lmList[tip_num][2] < lmList[tip_num - 2][2]:
    #             return True

    #     return False


def main():
    print("Please dont run this file!!!!")
    print("This is a package, it contains functions for your projects")
    print("Download it and import the handsDetector() class in another python project")
    print("Enjoy!!!")


if __name__ == "__main__":
    main()