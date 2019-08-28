from tkinter import *
import random
from time import gmtime, strftime
import os
import time
import tkinter.filedialog
from PIL import Image
import pytesseract
import argparse
import cv2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master) 
        Frame.config(self, bg="white")                
        self.master = master
        self.init_window()

    # Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("HOAX Search")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        text = Label(self, text="HOAX Search")
        text.config(bg="white", fg="black")
        text.place(relx=0.5, y=40, anchor=CENTER)

        text1 = Label(self, text="Brows Image:")
        text1.config(bg="white", fg="black")
        text1.place(x=20, y=60)

        btn = Button(root, text ='Open', command = self.open_file)
        btn.place(x=20, y=100) 

    def open_file(self): 
        global img_dir
        img_dir = tkinter.filedialog.askopenfilename()
        if len(img_dir) > 0:
            print("You chose %s" % img_dir)
            text1 = Label(self, text="You chose %s" % img_dir)
            text1.config(bg="white", fg="black")
            text1.place(x=120, y=105)
        image = cv2.imread(img_dir)
        while True:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)

            # load the image as a PIL/Pillow image, apply OCR, and then delete
            #the temporary file
            text = pytesseract.image_to_string(Image.open(filename))
            os.remove(filename)
            #print(text)

            f = open('../data/text.txt','a')
            f.write(text)

            # show the output images
            cv2.imshow("Image", image)
            #cv2.imshow("Output", gray)

            if len(text) > 1:
                break

        cv2.destroyAllWindows()
        search = Button(root, text ='Search', command = self.GetDataTitle)
        search.place(x=20, y=150) 

    def GetDataTitle(self):
        f=open(path + 'text.txt', "r")
        info =f.read()

        # get title
        get_title = info.split('.')
        global title
        title = get_title[0]
        #print(title)

        browser_path='../browser/geckodriver'
        driver = webdriver.Firefox(executable_path=browser_path)
        driver.get("https://www.google.com/")
        time.sleep(1)
        text_input = driver.find_element_by_xpath("//input[@type='text']")
        text_input.clear()
        text_input.send_keys(title)
        text_input.send_keys(Keys.RETURN)
        time.sleep(3)
        get_news = driver.find_element_by_xpath("//div[@class='r']").click()
        time.sleep(3)
        news_data = driver.find_elements_by_xpath("//body")
        time.sleep(2)
        
        with open(path + 'news.txt', "a") as news_file:
            for el in news_data:                 
                news_file.write(el.text+"\n")
                time.sleep(1)
                break
        driver.quit()

        # top delete
        f = open(path + 'news.txt', 'r')
        keyword = f.read().split()
        if 'kumparan' in keyword:
            data = open(path + 'news.txt', 'r')
            data_list = data.readlines()
            data.close()

            del data_list[0:32+1]
            #print(data_list)
            new = open(path + 'new.txt', 'a')
            new.writelines(data_list)
            new.close()
        if 'detikID' in keyword:
            data = open(path + 'news.txt', 'r')
            data_list = data.readlines()
            data.close()

            del data_list[0:26+1]
            #print(data_list)
            new = open(path + 'new.txt', 'a')
            new.writelines(data_list)
            new.close()

        # bottom delete
        f = open(path + 'news.txt', 'r')
        keyword = f.read().split()
        if 'kumparan' in keyword:
            f = open(path + 'new.txt', 'r')
            key = f.read().split('\n')
            element = 'Baca Lainnya'
            element = key.index(element)
            #print(element)
            f = open("../data/new.txt", "r")
            data_list = f.readlines()
            #print(data_list[0:element])
            fout = open(path + 'new1.txt', "a")
            fout.writelines(data_list[0:element])
            fout.close()
            
        if 'detikID' in keyword:
            f = open(path + 'new.txt', 'r')
            key = f.read().split('\n')
            element = 'Berita Terkait' or 'Baca Juga'
            element = key.index(element)
            #print(element)
            f = open("../data/new.txt", "r")
            data_list = f.readlines()
            #print(data_list[0:element])
            fout = open(path + 'new1.txt', "a")
            fout.writelines(data_list[0:element])
            fout.close()
            

        path_1 = '../data/text.txt'
        f1=open(path_1, "r")
        data1 =f1.read()
        s = data1.split()

        path_2 = '../data/new1.txt'
        f2=open(path_2, "r")
        data2 =f2.read()
        f = data2.split()

        ss= set(s)  
        fs =set(f)

        #print(ss.intersection(fs)) 
        #print(ss.union(fs)) 
        different = ss.union(fs) - ss.intersection(fs)
        total = len(s) + len(f) 

        score = len(different)/total*100
        print('Score by different: ' + str(score) + ' %')

        result = Label(self, text='Score by different: ' + str(score) + ' %')
        result.config(bg="white", fg="black")
        result.place(x=20, y=240)

        quitButton = Button(self, text="Done",command=self.client_exit)
        quitButton.place(x=20, y=280)

    def client_exit(self):
        exit()
               
path = '../data/'
root = Tk()
# size of the window
root.geometry("800x500+350+200")

root.overrideredirect(True)
root.overrideredirect(False)
app = Window(root)
root.wm_attributes("-topmost", 1)
root.mainloop()  