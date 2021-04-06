#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---

# Import required modules 

import requests 
from bs4 import BeautifulSoup
import re
import threading


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
        try:
            soup = BeautifulSoup(page.content,'html.parser')
            lista = soup.find('select','mangaread-page')
       
            epis = lista.findAll('option')
            caps = [int(x.text) for x in epis]

            return max(caps)
        except Exception as e: print('__conseguirCantidadPaginas'+str(e))


    def __subprocess(self,link,num,arr):
        try:
            print("este es el link mas importante"+link+str(num+1)+".html")
            page = requests.get(link+str(num+1)+".html") 
            
            s = BeautifulSoup(page.content,'html.parser')

            img = s.find(id="image")
            
            with self.lock:
                arr.append(img["src"])
        except Exception as e: print('__subprocess'+str(e))

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
                

                link2 = "https://m.mangahere.cc/"+"/".join([sp[3],sp[4],sp[5]])
      
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
        link = 'https://m.mangahere.cc/manga/'+name+'/'
        return link


#getrequestChap('https://www.mangatown.com/manga/','wortenia_senki',33)



