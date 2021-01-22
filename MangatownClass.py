#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---

# Import required modules 

import requests 
from bs4 import BeautifulSoup
import re
import threading


class Mangatown:
    def __init__(self,):
        self.lock = threading.Lock()
        self.Mangalink = ''
        self.manga_name = 'No Name'
        



    def getAllChapters(self,):
        try:
            page = requests.get(self.Mangalink) 
            s = BeautifulSoup(page.content,'html.parser')
            chaptersAll = s.find("ul","chapter_list")
            chaptersLinks = chaptersAll.find_all("li")
            arr = []
            for chap in chaptersLinks:
                arr.append('https://www.mangatown.com'+chap.a.get('href'))

            return arr
        except Exception as e: print('Mangatown getAllChapters:'+str(e))

    def __conseguirCantidadPaginas(self,page):

        num=re.search(r"total\_pages\s\=\s(\d+)",page.text)

        return int(num.group(1))
    def __subprocess(self,link,num,arr):
            page = requests.get(link+str(num+1)+".html") 
            s = BeautifulSoup(page.content,'html.parser')
            img = s.find(id="image")
            
            with self.lock:
                arr.append(img["src"])

    def __conseguirimagen(self,link,paginas):
        arr = []
        jobs = []
        
        for num in range(paginas):
            x = threading.Thread(target=self.__subprocess, args=(link,num,arr,))
            jobs.append(x)
            x.start()
        for  x in jobs:
            x.join()
        arr.sort()
        
        return(arr)


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
            
            page = requests.get(Fulllink) 
            paginas = self.__conseguirCantidadPaginas(page)
            links = self.__conseguirimagen(Fulllink,paginas)
            
            return links
        except Exception as e: print("mangatown getrequestChap: "+str(e))

  
    def parselink(self,link):
        try:
            
            sp = link.split('/')
            if len(sp) < 7:
                

                link = "https://www.mangatown.com/"+"/".join([sp[3],sp[4],sp[5]])
                print("este es el linl que se guarda "+link)
                self.Mangalink = link
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
        link = 'https://www.mangatown.com/manga/'+name+'/'
        return link


#getrequestChap('https://www.mangatown.com/manga/','wortenia_senki',33)

