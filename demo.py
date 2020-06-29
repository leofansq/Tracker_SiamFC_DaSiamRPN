"""
Demo
@ fansiqi 2020.4.22
"""
from tkinter import *
from tkinter.filedialog import askopenfilename

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
from time import time

from SiamFC.tracker import TrackerSiamFC
from DaSiamRPN.tracker import TrackerDaSiamRPN

def get_dir(path):
    _path = askopenfilename()
    path.set(_path)


def demo(path, model_name):
    """
    Demo
    Parameters:
        path: path of video
        model_name: 'SiamFC' or 'DaSiamRPN'
    """
    #Load Model
    if model_name == 'SiamFC':
        tracker = TrackerSiamFC("./SiamFC/SiamFC.pth") 
    elif model_name == 'DaSiamRPN':
        tracker = TrackerDaSiamRPN("./DaSiamRPN/DaSiamRPN.pth")
  
    # Select ROI
    cap = cv2.VideoCapture(path)
    cv2.namedWindow(model_name, cv2.WND_PROP_FULLSCREEN)
    success, frame = cap.read()

    select_flag = False # Deal with the cancel of ROI selection 
    while success and not select_flag:
        x, y, w, h = cv2.selectROI(model_name, frame, False, False)
        if w and h :
            select_flag = True
            box = [x, y, w, h]
        print (x, y, w, h)

    # Init Tracker
    tracker.init(frame, box)
    
    # Track & Visualization
    while True:
        success, frame = cap.read()
        if not success: break

        pred = tracker.update(frame)

        cv2.rectangle(frame, (int(pred[0]), int(pred[1])), (int(pred[0] + pred[2]), int(pred[1] + pred[3])), (0, 255, 255), 3)
        cv2.imshow(model_name, frame)

        # Interaction during video
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):break
        elif key == ord('p'): cv2.waitKey()
        elif key == ord('s'): cv2.imwrite("./{}.png".format(time()), frame)
    
    cv2.destroyAllWindows()


def ui():
    """
    Demo UI
    """
    # Window
    root = Tk()
    root.title('Demo')
    root.geometry('300x300')
    root.resizable(0,0) 

    # Select Video
    path = StringVar()

    Label(root, text = "Step 1: Select a video", width=30).place(x=10, y=30)
    Entry(root, textvariable = path, background = 'white', width=30).place(x=40, y=55)
    Button(root, text = "Select", command = lambda:get_dir(path), width=27).place(x=40, y=75)

    # Select Model
    Label(root, text = "Step 2: Select a model", width=30).place(x=10, y=110)
    Button(root, text = "SiamFC", command = lambda:demo(path.get(), 'SiamFC'), width = 11).place(x=42, y=130)
    Button(root, text = "DaSiamRPN", command = lambda:demo(path.get(), 'DaSiamRPN'), width = 11).place(x=150, y=130)

    # Tips
    Label(root, text = "Step 3:\n  Select a ROI and then press SPACE or ENTER.\n  Cancel the selection process by pressing 'c'. ", wraplength=220, justify = 'left', width=30).place(x=40, y=165)
    Label(root, text = "Press 'q' to QUIT during video. Press 'p' to PAUSE and press any key to continue. Press 's' to SAVE the image.", wraplength=220, justify = 'left', width=31).place(x=40, y=235)

    root.mainloop()

if __name__ == "__main__":
    ui()