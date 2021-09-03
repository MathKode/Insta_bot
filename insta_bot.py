from typing import Mapping
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

class Bot():
    def __init__(self,username,password):
        try :
            self.driver = webdriver.Chrome()
            self.driver.get("https://www.instagram.com/")

            self._pop_up1()
            print('pop up ok')
            self._auth(username,password)
            print("auth ok")

        except:
            print("Erreur")

    # --- Authentification Zone ---
    def _pop_up1(self):
        click=True
        while click:
            try :
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]").click()
                click=False
            except :
                time.sleep(1)
    def _auth(self,username,password):
        click=True
        while click:
            try :
                name_entry = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
                pass_entry = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
                button = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]")
                click=False
            except :
                time.sleep(1)
        name_entry.send_keys(username)
        pass_entry.send_keys(password)
        button.click()
    # -----------

    # --- Navigate ---
    def go_to(self,profil_name):
        self._open_bar()
        self._write_bar(profil_name)
        elements = self._result_find()
        name = elements[0].text.split('\n')[0]
        self._valid(1)
        self._wait_charging_profile(name)
    def find_and_go(self,text_to_search,line_number):
        self._open_bar()
        self._write_bar(text_to_search)
        self._valid(int(line_number))
    def find_and_get(self,text_to_search):
        #return a list of the profile name when you search the text
        self._open_bar()
        self._write_bar(text_to_search)
        elements = self._result_find()
        ls = []
        for i in elements:
            ls.append(i.text)
        self._close_bar()
    def _open_bar(self):
        i = True
        while i:
            try :
                self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[1]").click()
                i = False
            except:
                print("Wait Charging site",end="\r")
        print("Site Charged         ")
    def _write_bar(self,message):
        bar = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        bar.send_keys(message)
    def _valid(self,profil_number):
        r = self._result_find()
        if len(r) > profil_number-1:
            el = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
            el.send_keys(Keys.ENTER)
            for i in range(profil_number-1):
                el.send_keys(Keys.DOWN)
            el.send_keys(Keys.ENTER)
    def _result_find(self):
        i = True
        tour = 0
        while i:
            try :
                elements = self.driver.find_elements_by_class_name("-qQT3")
                if len(elements) >= 1 or tour == 1000:
                    i = False
                else :
                    tour += 1
            except :
                time.sleep(1)
        if tour == 1000:
            print('Time out')
            return []
        else :
            return elements
    def _close_bar(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]").click()
    def _wait_charging_profile(self,name):
        i = True
        while i:
            try:
                name_actuel = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/h2").text
                if name_actuel == name:
                    i = False
            except:
                time.sleep(1)
    # --------

    # Profil information
    def get_follower_number(self,name):
        stat = self.get_profil_info(name)
        abo = stat[1]
        t = 1000
        result=0
        for i in ["k","m"]:
            if str(abo).lower()[-1] == i:
                result=int(float(".".join(str(abo)[:-1].split(',')))*t)
            t = t*1000
        if result==0:
            result=int(stat[1])
        return result    
    def get_profil_info(self,name):
        # Get a list like this ['33 470', '3,2m', '160']
        # [publication, followers, followed]
        self.go_to(name)
        i = True
        while i:
            try :
                stat = self.driver.find_elements_by_class_name("g47SY ")
                if len(stat) > 1:
                    i = False
            except:
                time.sleep(1)
        ls = []
        for i in stat:
            ls.append(i.text)
        return ls 
    def get_profil_name(self):
        try:
            return self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/h2").text
        except:
            return 0 #Quand il n'est pas sur un profil
    def get_follower_list(self,profil_name):
        follower_nb = self.get_follower_number(profil_name)
        self._open_followerlist()
        i = True
        while i:
            try:
                liste = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
                i = False
            except:
                i = True
        i = True
        while i:
            try :
                elements = self.driver.find_elements_by_class_name("wo9IH")
                print(len(elements),int(follower_nb)-1,end='\r')
                if len(elements) >= int(follower_nb)-1:
                    print(len(elements),int(follower_nb)-1)
                    i = False
                else :
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', liste)
            except:
                i = True
        ls = []
        for i in elements:
            try :
                ls.append(str(i.text).split("\n")[0])
            except :
                print("Erreur with",i,i.text)
        self._close_followerlist()
        return ls
    def _open_followerlist(self):
        i = True
        while i:
            try :
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
                i = False
            except:
                i = True
    def _close_followerlist(self):
        i = True
        while i:
            try :
                self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button/div").click()
                i = False
            except:
                i = True
        

        


b = Bot("faibash.57","bubul2017")
print(b.get_follower_list("math.k57"))
print(b.get_follower_list("lun4r_dev"))
time.sleep(1000)