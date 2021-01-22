#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---

# Import required modules 

from MangatownClass import Mangatown
from MangahereClass import Mangahere

class MangaTodo:
    def __init__(self,):

        self.valor = 0
        a = Mangatown()
        b = Mangahere()
        self.__TodasClases = ["",a,b]

        

    def __Identificar(self,link):
        if ('mangatown' in link):
            tipo = 1
        elif 'mangahere' in link:
            tipo = 2
        else:
            tipo = 0
        self.valor = tipo
        return tipo

    def getAllChapters(self,):
        print("esto es test",self.__TodasClases[self.valor])
        return self.__TodasClases[self.valor].getAllChapters()

    def getChapter(self,num):
        return self.__TodasClases[self.valor].getChapter(num)

    def parselink(self,link):
        iden = self.__Identificar(link)
        print(self.__TodasClases, iden)
        funcArray = self.__TodasClases[iden].parselink(link)
        funcArray[0] =  funcArray[0]+" "+str(iden)
        return funcArray
    def recontruccion(self,name):
        val = name.split(" ")
        iden = int(val[-1])
        return self.__TodasClases[iden].recontruccion(val[0])
        

