import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

def GetDataTitle():
    f=open(path + 'text.txt', "r")
    info =f.read()

    # get title
    get_title = info.split('.')
    global title
    title = get_title[0]
    print(title)

def WebSearch():
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

def TopDel():
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

def BottomDel():
    f = open(path + 'news.txt', 'r')
    keyword = f.read().split()
    if 'kumparan' in keyword:
        f = open(path + 'new.txt', 'r')
        key = f.read().split('\n')
        element = 'Baca Lainnya'
        element = key.index(element)
        #print(element)
        f = open("./data/new.txt", "r")
        data_list = f.readlines()
        #print(data_list[0:element])
        fout = open(path + 'new1.txt', "a")
        fout.writelines(data_list[0:element])
        fout.close()
        os.remove('./data/new.txt')
        os.remove('./data/news.txt')
    if 'detikID' in keyword:
        f = open(path + 'new.txt', 'r')
        key = f.read().split('\n')
        element = 'Berita Terkait'
        element = key.index(element)
        #print(element)
        f = open("./data/new.txt", "r")
        data_list = f.readlines()
        #print(data_list[0:element])
        fout = open(path + 'new1.txt', "a")
        fout.writelines(data_list[0:element])
        fout.close()
        os.remove('./data/new.txt')
        os.remove('./data/news.txt')

path = '../data/'
GetDataTitle()
WebSearch()
time.sleep(2)
TopDel()
BottomDel()