from tensorflow.keras.models import load_model
from tkinter import *
from tkinter.ttk import *
import time
import cv2
import Code.camera as camera
import os
#from message_box import message_Box as mesg
from PIL import Image, ImageTk
import warnings
import traceback
warnings.filterwarnings("ignore")
warnings.filterwarnings("error")


master = Tk()
# setting window size
master.state("zoomed")
# Giving Title name of Window
master.title("ATM SECURITY ENHANCEMENT USING COMPUTER VISION")

################################### functions to be created ########################################
class gui_maker():
    
    prototxtPath=None
    weightsPath=None
    faceNet=None
    cover_model=None
    filename=None
    entry_time=None

    def __init__(self):
        try:
            # loading of classifier for face detection
            # getting prototxtPath file
            self.prototxtPath = r".\Model\deploy.prototxt"
            # getting weightsPath file
            self.weightsPath = r".\Model\res10_300x300_ssd_iter_140000.caffemodel"
            self.faceNet = cv2.dnn.readNet(self.prototxtPath, self.weightsPath)
            
            # getting cover model file and loading it 
            self.cover_model = load_model(r".\Model\mask_detector.model") 
        except Exception as ex:
            traceback.print_exc()
    
    def cash_wd():
        return


    def Balance():
        return

    def camera_face_detect(self):
        try:
            # calling camera class 
            fd = camera.faceDetection()
            # Starting detecting of face
            f = fd.start(self.faceNet, self.cover_model, master)
            if f == True:
                self.pin_win()
        except Exception as ex:
            traceback.print_exc()

    def main_menu(self):
        try:
            main = Toplevel(master)
            # Setting window size
            main.state("zoomed")
            # Creating Cash Withdraw button
            Button(main, text="Cash withdraw").pack()
            # Creating Min Statement button
            Button(main, text="Mini Statement").pack()
            # Creating Balance Info button
            Button(main, text="Balance Info").pack()

            main.mainloop()
        except Exception as ex:
            traceback.print_exc()
        
# function to check pin..........................
    def pin_win(self):
        try:
        # HERE WE ARE TAKING PIN AND WILL CHECK THE PIN.....
            global win4
            win4 = Toplevel(master)
            # setting window size
            win4.state("zoomed")
            
            # background image
            # image = Image.open("pin_window.jpg")
            # bg = ImageTk.PhotoImage(image)
            Label(win4).place(relwidth=1, relheight=1)
            
            # Creating Label
            Label(win4, text="Enter your unique pin below").pack()
            
            global pin
            # Creating password entry
            pin = Entry(win4, show="*")
            pin.pack(ipadx=50)
            
            # creating enter button
            enter = Button(win4, text="Enter",command=lambda:self.pin_check())
            enter.pack()

            # creating back button
            back = Button(win4, text='back', command=lambda : win4.destroy())
            back.pack()
        except Exception as ex:
            traceback.print_exc()

    def pin_check(self):
        try:
            psswd=pin.get()
            # checking for pin enter 
            if psswd=='1234':
                pin.destroy()
                self.main_menu()
            #else:
            # mesg.show_error(master=master, text="worng pin")
        except Exception as ex:
            traceback.print_exc()

    def main():
        try:
            f = gui_maker()
            # creating label 
            label1 = Label(master, text="STATE BANK OF INDIA", font=("Bell MT", 60))
            label1.grid(row=0, column=0, padx=300, pady=100)

            # Creating Start Button
            bt1 = Button(master, text="Start", command=lambda:f.camera_face_detect())
            bt1.grid(row=1, column=0)
            mainloop()
        except Exception as ex:
            traceback.print_exc()

