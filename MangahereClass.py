#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---

# Import required modules 

import requests 
from bs4 import BeautifulSoup
import re
import threading
import glob
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# esto es para selenium 4.0 y poder utilizar flags para asi eliminar la consola en windows
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import sys
import wget
import zipfile
from pathlib import Path
import time

if hasattr(sys, "frozen"):
    main_dir = os.path.dirname(sys.executable)
    full_real_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    script_dir = os.path.dirname(__file__)
    main_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    full_real_path = os.path.dirname(os.path.realpath(sys.argv[0]))



class Mangahere:
    def __init__(self,):
        self.lock = threading.Lock()
        self.cantidadCaps = 0
        self.Mangalink = ''
        self.manga_name = 'No Name'
        

    def ConseguirCOVER(self,):
        try:
            print("link de "+self.Mangalink)
            pagina = requests.get(self.Mangalink) 
            print("ok")
            s = BeautifulSoup(pagina.content,'html.parser')
            print("ok")
            img = s.find("img",{"class","detail-cover"})
            print(img)
            link = img['src']

            return link
        except Exception as e: print('Imagen:'+str(e))

    def getAllChapters(self,):
        try:
            print("link de "+self.Mangalink)
            print("Consiguiendo capitulos")
            page = requests.get(self.Mangalink) 
            
            s = BeautifulSoup(page.content,'html.parser')
            
            ss = s.find("div","manga-chapters")
            chaptersAll = ss.find("ul")
           # print(chaptersAll)
            chaptersLinks = chaptersAll.find_all("li")
            arr = []
            for chap in chaptersLinks:
                #sacando el 1.html del link
                
                extension =  chap.a.get('href')
                if len(extension.split('/')) == 7:
                    arr.append('https:'+extension)
                #print(extension)
     
            self.cantidadCaps = arr[0].split('/')[-2][1:]

            return arr
        except Exception as e: print('Mangatown getAllChapters:'+str(e))

    def __conseguirCantidadPaginas(self,page):
        # esta modificacion es por que la pagina ahora usa https://newm. en vez de lo otro, solo se arreglo
        try:
            todo = page.text
           
            m = re.search(r'imagecount\=(\d+)', todo)
            #imagecount=35
            print("#####################")
            print(m.group(1))
            print("#####################")
            caps = range(1,int(m.group(1))+1)
            return max(caps)
            '''
            soup = BeautifulSoup(page.content,'html.parser')
            lista = soup.find('select','mangaread-page')
       
            epis = lista.findAll('option')
            caps = [int(x.text) for x in epis]

            return max(caps)
            '''
        except Exception as e: print('__conseguirCantidadPaginas'+str(e))


    def __subprocess(self,link,num,arr,driver,pathchap,cap,muta):
        # esta modificacion es por que la pagina ahora usa https://newm. en vez de lo otro, solo se arreglo
        try:

            pagina = link+str(num+1)+".html"
        
            driver.get(pagina) 

            boton = WebDriverWait(driver, 20).until( EC.presence_of_element_located((By.XPATH,"//html/body/div[4]/img[contains(@src,'jpg') or contains(@src,'jpeg')]")))
            s = BeautifulSoup(driver.page_source,'html.parser')
            img = s.find('img',{'class':'reader-main-img'})
            
            newpath = os.path.join(pathchap,str(num+1)+".jpg")
            print(newpath)
            
            with open(newpath,"wb") as f:
                f.write(requests.get("http:"+img["src"]).content)
            if muta:
                sss="/static/tempImages/"+self.manga_name+"/"+cap+"/"+str(num+1)+".jpg"
                arr.append(sss)
            
        except:
            pass
        
        ###############################
        '''
        try:

            pagina = link+str(num+1)+".html"
            page = requests.get(pagina) 
            print(pagina)
            s = BeautifulSoup(page.content,'html.parser')
            img = s.find('img',{'class':'reader-main-img'})
            with self.lock:
                arr.append(img["src"])

        except Exception as e: print('__subprocess'+str(e))
        '''

    def __conseguirimagen(self,link,paginas,cap):
        newpath = os.path.join(full_real_path,"static","tempImages",self.manga_name,cap)
        arr = []
        if os.path.exists(newpath):     

            arr =[os.path.join("static","tempImages",self.manga_name,cap,filename) for filename in os.listdir(newpath) if filename.endswith(".jpg")]

        else:
            os.makedirs(newpath)
            opt = Options() 
            opt.add_argument("--headless")  
        
            camino = self.download_chromedriver()
            chrome_service = ChromeService(camino)
            driver = webdriver.Chrome(service=chrome_service,options=opt)
            
            pagina = link+str(1)+".html"
            driver.get(pagina) 
            
            try:
                boton = WebDriverWait(driver, 7).until( EC.presence_of_element_located((By.ID,"checkAdult")))
                boton.click()   
            except:
                print("no +18")

            for num in range(paginas):
                self.__subprocess(link,num,arr,driver,newpath,cap,True)
            
            jobs = []
            ######################################
            test = self.getAllChapters()
            newcap = ""
            largo = len(test)
            for x in range(largo):
                if (cap in test[x]) and (x-1 >=0):
                    newcap = test[x-1].split('/')[-2]
                    print("#%"*8+newcap)
                    break

            if newcap != "":
                newpath = os.path.join(full_real_path,"static","tempImages",self.manga_name,newcap)
    
                if not os.path.exists(newpath):     
                    
                    os.makedirs(newpath)
                    Fulllink = self.Mangalink + newcap+'/'
                    
                    Fulllink2 = "https://newm."+".".join(Fulllink.split('.')[1:])
                    page = requests.get(Fulllink2) 
                    pagina2 = Fulllink2+str(1)+".html"
                 
                    driver.get(pagina2) 
                    try:
                        boton = WebDriverWait(driver, 7).until( EC.presence_of_element_located((By.ID,"checkAdult")))
                        boton.click()   
                    except:
                        print("no +18")
                    paginas = self.__conseguirCantidadPaginas(page)
                    for num2 in range(paginas):
                       self.__subprocess(Fulllink2,num2,0,driver,newpath,newcap,False)
            driver.close
                 
        
        return arr
                


            
        


    def getChapter(self,numCap):
        try:
            """
            if numCap < 10:
                cap = "00"+str(numCap)
            elif numCap < 100:
                cap = "0"+str(numCap)
            else:
                cap = str(numCap)
            """
            Fulllink = self.Mangalink + numCap+'/'
            
            Fulllink2 = "https://newm."+".".join(Fulllink.split('.')[1:])

            print("este es fulllonk" +Fulllink2)
            page = requests.get(Fulllink2) 
            paginas = self.__conseguirCantidadPaginas(page)
            links = self.__conseguirimagen(Fulllink2,paginas,numCap)
            
            return links
        except Exception as e: print("mangatown getrequestChap: "+str(e))

  
    def parselink(self,link):
        try:
            
            sp = link.split('/')
            
            if len(sp) < 7:
                

                link2 = "https://m.mangahere.cc/"+"/".join([sp[3],sp[4],sp[5]])
                
                print(link2)
                self.Mangalink = link2
                nombremanga = sp[-2]
                self.manga_name = nombremanga
                return [nombremanga]
            elif len(sp) < 8:
                nombremanga = sp[-3]
                cap = sp[-2]
           
                #self.manga_name = nombremanga
                return [nombremanga,cap]
        except Exception as e: print('mangatown parselink'+str(e))

    def recontruccion(self,name):
        #https://newm.mangahere.cc/manga/hagure_idol_jigokuhen/c001/1.html
        link = 'https://m.mangahere.cc/manga/'+name+'/'
        return link

    def download_chromedriver(self,):
        def get_latestversion(version):
            url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + str(version)
            response = requests.get(url)
            version_number = response.text
            return version_number

        def download(download_url, driver_binaryname, target_name,path):
            # download the zip file using the url built above
            latest_driver_zip = wget.download(download_url, out=os.path.join(path,'temp/chromedriver.zip'))

            # extract the zip file
            with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
                zip_ref.extractall(path = os.path.join(path,'temp/')) # you can specify the destination folder path here
            # delete the zip file downloaded above
            os.remove(latest_driver_zip)
            os.rename(driver_binaryname, target_name)
            os.chmod(target_name, 0o755)
        if os.name == 'nt':
            replies = os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
            replies = replies.split('\n')
            camino = r"C:\Users\Public\Automeet"
            Path(camino).mkdir(parents=True, exist_ok=True)
            Path(os.path.join(camino,'temp')).mkdir(parents=True, exist_ok=True)
            Path(os.path.join(camino,'bin')).mkdir(parents=True, exist_ok=True)

            for reply in replies:
                if 'version' in reply:
                    reply = reply.rstrip()
                    reply = reply.lstrip()
                    tokens = re.split(r"\s+", reply)
                    fullversion = tokens[len(tokens) - 1]
                    tokens = fullversion.split('.')
                    version = tokens[0]
                    break
            target_name = os.path.join(camino,'bin/chromedriver-win-' + version + '.exe')
            found = os.path.exists(target_name)
            if not found:
                version_number = get_latestversion(version)
                # build the donwload url
                download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"
                download(download_url, os.path.join(camino,'temp/chromedriver.exe'), target_name,camino)

        elif os.name == 'posix':
            reply = os.popen(r'Chrome --version').read()

            Path(os.path.join(full_real_path,'temp')).mkdir(parents=True, exist_ok=True)
            Path(os.path.join(full_real_path,'bin')).mkdir(parents=True, exist_ok=True)
            
            if reply != '':
                reply = reply.rstrip()
                reply = reply.lstrip()
                tokens = re.split(r"\s+", reply)
                fullversion = tokens[1]
                tokens = fullversion.split('.')
                version = tokens[0]
            else:
                reply = os.popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version').read()
                reply = reply.rstrip()
                reply = reply.lstrip()
                tokens = re.split(r"\s+", reply)
                fullversion = tokens[2]
                tokens = fullversion.split('.')
                version = tokens[0]
            print("probando")
            
            target_name = os.path.join(full_real_path,'bin/chromedriver-linux-'+version)
            print('new chrome driver at ' + target_name)
            found = os.path.exists(target_name)
            if not found:
                version_number = get_latestversion(version)
                download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_mac64.zip"
                print("ya voy aca")
                download(download_url, os.path.join(full_real_path,'temp/chromedriver'), target_name,full_real_path) 
        print(target_name)
        return target_name


#getrequestChap('https://www.mangatown.com/manga/','wortenia_senki',33)



