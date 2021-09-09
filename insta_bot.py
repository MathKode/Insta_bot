from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

class Bot():
    def __init__(self,username,password,path):
        try :
            if path == "":
                self.driver = webdriver.Chrome()
            else :
                self.driver = webdriver.Chrome(executable_path=path)
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
                name_entry.send_keys(username)
                pass_entry.send_keys(password)
                button.click()
                click=False
            except :
                time.sleep(1)
        
    # -----------

    # --- Navigate ---
    def go_to(self,profil_name):
        try :
            n = self.get_profil_name()
        except :
            n = ""
        if n != profil_name:
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
        return ls
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
        i = True
        while i:
            try:
                bar = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
                bar.send_keys(message)
                i = False
            except:
                i = True
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
        i = True
        while i:
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]").click()
                i=False
            except:
                i=True
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
    def get_followed_number(self,name):
        stat = self.get_profil_info(name)
        return stat[2]
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
    def get_follower_list(self,profil_name,end):
        #follower_nb = self.get_follower_number(profil_name)
        self.go_to(profil_name)
        self._open_followerlist()
        ls = self._finish_fonction("/html/body/div[6]/div/div/div[2]",end)
        self._close_followerlist()
        return ls
    def get_followed_list(self,profil_name,end):
        #followed_nb = self.get_followed_number(profil_name)
        self.go_to(profil_name)
        self._open_followedlist()
        ls = self._finish_fonction("/html/body/div[6]/div/div/div[3]",end)
        self._close_followedlist()
        return ls
    def get_profil_state(self,profil_name): #retourn True = public, False = private
        self.go_to(profil_name)
        self.get_profil_name()
        try :
            self.driver.find_element_by_class_name("rkEop")
            return False
        except :
            return True
    def _finish_fonction(self,path_to_list,end):
        i = True
        while i:
            try:
                liste = self.driver.find_element_by_xpath(str(path_to_list))
                i = False
            except:
                i = True
        i = True
        old=0
        wait=0
        while i:
            try :
                elements = self.driver.find_elements_by_class_name("wo9IH")
            except:
                elements=[]
            if wait >= end*10:
                i = False
            if len(elements) != old:
                wait = 0
                old = len(elements)
            else :
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', liste)
                wait += 1
                time.sleep(0.1)
            print(wait,end='\r')
        ls = []
        for i in elements:
            try :
                ls.append(str(i.text).split("\n")[0])
            except :
                print("Erreur with",i,i.text)
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
    def _open_followedlist(self):
        i = True
        while i:
            try :
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a").click()
                i = False
            except:
                i = True
    def _close_followedlist(self):
        i = True
        while i:
            try :
                self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button").click()
                i = False
            except:
                i = True
    # --------

    # --- Developpers ---
    def get_driver(self):
        return self.driver
    def url(self):
        i = True
        while i:
            try:
                url = self.driver.current_url
                i = False
            except:
                i = True
        return url
    def close(self):
        self.driver.quit()
    # --------

    # --- Messages ---
    def open_message(self):
        url = self.url()
        if url != "https://www.instagram.com/direct/inbox/" and len(url.split('direct/t')) == 1:
            i = True
            while i:
                try:
                    self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a").click()
                    i = False
                except:
                    i = True
            i = True
            while i:
                try:
                    self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]").click()
                    i = False
                except:
                    i = True
        else:
            print('Tu es déjà dans la messagerie')
            i = True
            t = 0
            while i:
                try:
                    self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]").click()
                    i = False
                except:
                    i = True
                    t += 1
                if t == 100:
                    i = False
    def get_conversation_list(self):
        self.open_message()
        i = True
        while i:
            try:
                el = self.driver.find_element_by_xpath(f"/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[1]/a/div/div[2]/div[1]/div/div/div/div")
                dm = self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div")
                i = False
            except:
                i = True
        ls = []
        i = True
        tour = 1
        wait = 0
        tt = 0
        while i:
            try :                                                                                                    
                el = self.driver.find_element_by_xpath(f"/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[{tour-tt}]/a/div/div[2]/div[1]/div/div/div/div")
                ls.append(el.text)
                wait = 0
                tour += 1
            except :
                try :
                    self.driver.execute_script('arguments[0].scrollBy(0,100)', dm)
                    wait += 1
                except:
                    m=3
            if int(wait) == 30:
                i = False
            try :
                el = self.driver.find_element_by_xpath(f"/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[1]/a/div/div[2]/div[1]/div/div/div/div")
                #print(el,tour,ls,end='\r')
                if el.text in ls:
                    t = 0
                    for j in ls:
                        if j == el.text:
                            tt = t
                        t += 1
            except:
                m=3
            time.sleep(0.1)
            print(wait,tour,tt,end="\r")
        return ls
    def send_to(self,profil_name,message):
        self.open_message()
        self._open_messagebar()
        self._write_messagebar(profil_name)
        self._validuser_messagebar()
        self._valid_messagebar()
        self._write_message(message)
        self._send()
    def send_to_group(self,groupls,message):
        self.open_message()
        self._open_messagebar()
        for i in groupls:
            self._write_messagebar(i)
            self._validuser_messagebar()
            time.sleep(1)
        self._valid_messagebar()
        self._write_message(message)
        self._send()
    def last_message(self,profil_name):
        self.open_message()
        self._open_messagebar()
        self._write_messagebar(profil_name)
        self._validuser_messagebar()
        self._valid_messagebar()
        time.sleep(1)
        i = True
        while i:
            try:
                el = self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div")
                i = False
            except:
                i = True
        ls = el.text.split('\n')
        return ls

    def _open_messagebar(self):
        i = True
        while i:
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button").click()
                i = False
            except:
                i = True
    def _write_messagebar(self,message): #Mets le nom
        i = True
        while i:
            try:
                el = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input")
                el.send_keys(str(message))
                i = False
            except:
                i = True
    def _validuser_messagebar(self): #Valid l'user
        i = True
        while i:
            try:
                self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div/div[3]/button").click()
                i = False
            except:
                i = True
    def _valid_messagebar(self): #Clique sur démarrer une discussion
        i = True
        while i:
            try:
                self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/div/button").click()
                i = False
            except:
                i = True
    def _write_message(self,message):
        i = True
        while i:
            try:
                el = self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
                el.send_keys(message)
                i = False
            except:
                i = True
    def _send(self):
        i = True
        while i:
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button").click()
                i = False
            except:
                i = True
    # --------

    # --- Test ---
    def _Test_Scroll(self):
        #Ceci est un test de scroll par pixel (ne sert a rien)
        self.open_message()
        time.sleep(3)
        dm = self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div")
        dm = self.driver.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]")
        time.sleep(3)
        while True:
            self.driver.execute_script('arguments[0].scrollBy(0,100)', dm)
    # --------