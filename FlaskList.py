#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---

# Import required modules 
import TodoMangas
import pickle
from flask import Flask,render_template,request
import os

app = Flask(__name__)
path = os.path.dirname(os.path.realpath(__file__))
MangaT = TodoMangas.MangaTodo()

@app.route('/')
def index():
    data = check()
    new  = []
    for x in data.keys():
        new.append([MangaT.recontruccion(x),x])
    
    return render_template('index.html',header='Amazing Universe', sub_header='Our universe is quite amazing', list_header="Galaxies!",
                    galaxies=new, site_title="Camposha.info")

@app.route('/usuario',methods=['POST'])

def usuario():
    data = check()
    parts = []
    nombreUser = request.form['Link']
    ##
    todos = MangaT.getAllChapters()
    ##
    parts = MangaT.parselink(nombreUser)
    indice = todos.index(nombreUser)
    if indice < len(todos)-1:
        prevchap =  todos[indice+1]
    else:
        prevchap = ''
    ##########################
    if indice > 0:
        nextchap =  todos[indice-1]
    else:
        nextchap = ''
    ##########################
    if parts[1] not in data[parts[0]]:
        data[parts[0]].append(parts[1])
        add(data)
        status = 'No Visto'
    else:
        status = 'Visto'
    
    array = MangaT.getChapter(parts[1])  
    return render_template('mangaCap.html',linkHome='http://127.0.0.1:5000/',header=parts[0], sub_header=parts[1], list_header=status,
                        galaxies=array, site_title=parts[0], nextchap = nextchap, prevchap = prevchap)

@app.route('/AddManga',methods=['POST'])

def AddManga():
    data = check()
    link = request.form['Link']
    status = ''
 
    parts = MangaT.parselink(link)

    if parts[0] not in data.keys():
        data[parts[0]]=[]
        add(data)
        status = 'Agregado'
    else:
        status = 'Ya existe'
 
    array = MangaT.getAllChapters() 
    
    newarray = [[x,''] if MangaT.parselink(x)[1] in data[parts[0]] else [x,'No Visto'] for x in array]




    return render_template('mangaFull.html',header=status, linkHome='http://127.0.0.1:5000/', list_header="Galaxies!",
                       galaxies=newarray, site_title="Manga")



def add(data):

    file = open(os.path.join(path,'important'), 'wb')

    # dump information to that file
    pickle.dump(data, file)

    # close the file
    file.close()

def check():
    try:
        print(os.path.join(path,'important'))
        file = open(os.path.join(path,'important'), 'rb')
        # dump information to that file
        data = pickle.load(file)

        # close the file
        file.close()
    except:
        data = {}
    return data



if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)