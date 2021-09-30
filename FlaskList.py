#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---

# Import required modules 
import TodoMangas
from flask import Flask,render_template,request
import os
import json
import requests
import pickle
import webbrowser
import sys
import shutil

app = Flask(__name__)
path = os.path.dirname(os.path.realpath(__file__))
MangaT = TodoMangas.MangaTodo()

if hasattr(sys, "frozen"):
    main_dir = os.path.dirname(sys.executable)
    full_real_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    script_dir = os.path.dirname(__file__)
    main_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    full_real_path = os.path.dirname(os.path.realpath(sys.argv[0]))

def eliminar():
    folder = os.path.join(full_real_path,"static","tempImages")
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@app.route('/')
def index():
    print("aca")
    data = check()
    print("aca")
    new  = []
    for x in data.keys():
        print(data[x][0])
        
        if not os.path.exists(os.path.join(path,"static/"+x+".jpeg")):
            r = requests.get("http:"+data[x][0], allow_redirects=True)
            with open(os.path.join(path,"static/"+x+".jpeg"), 'wb') as f:
                f.write(r.content)
        new.append([MangaT.recontruccion(x),x,"/static/"+x+".jpeg"])
    eliminar()
    return render_template('index.html',header='Amazing Universe', sub_header='Our universe is quite amazing', list_header="Galaxies!",
                    galaxies=new, site_title="MangaSeba")

@app.route('/',methods=['POST'])
def delete():
    data = check()
    
    nombreUser = request.form['delete']
    data.pop(nombreUser, None)
    add(data)
    new  = []
    for x in data.keys():
        new.append([MangaT.recontruccion(x),x,"/static/"+x+".jpeg"])
    eliminar()
    return render_template('index.html',header='Amazing Universe', sub_header='Our universe is quite amazing', list_header="Galaxies!",
                    galaxies=new, site_title="MangaSeba")


@app.route('/usuario',methods=['POST'])

def usuario():
    data = check()
    parts = []
    nombreUser = request.form['Link']
    ##

    todos = MangaT.getAllChapters()
    ##
    parts = MangaT.parselink(nombreUser)
    print(parts)
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
        data[parts[0]][1].append(parts[1])
        add(data)
        status = 'No Visto'
    else:
        status = 'Visto'
    title = parts[0].split(',')[0]
    array = MangaT.getChapter(parts[1])  
    return render_template('mangaCap.html',linkHome='http://127.0.0.1:5000/',header=title, sub_header=parts[1], list_header=status,
                        galaxies=array, site_title=title, nextchap = nextchap, prevchap = prevchap)

@app.route('/AddManga',methods=['POST'])

def AddManga():
    data = check()
    link = request.form['Link']
    status = ''

    parts = MangaT.parselink(link)
    linkcover = MangaT.ConseguirCOVER()
    print(parts)
    if parts[0] not in data.keys():
        data[parts[0]]=[linkcover,[]]
        add(data)
        status = 'Agregado'
    else:
        status = 'Ya existe'
 
    array = MangaT.getAllChapters() 
    
    newarray = [[x,''] if MangaT.parselink(x)[1] in data[parts[0]][1] else [x,'No Visto'] for x in array]




    return render_template('mangaFull.html',header=status, linkHome='http://127.0.0.1:5000/', list_header=parts[0],
                       galaxies=newarray, site_title="Manga")



def add(data):

    file = open(os.path.join(path,'important'), 'wb')

    # dump information to that file
    #json.dump(data, file)
    pickle.dump(data, file)

    # close the file
    file.close()

def check():
    try:
        print(os.path.join(path,'important'))
        file = open(os.path.join(path,'important'), 'rb')
        # dump information to that file
        data = pickle.load(file)
        #data = json.loads(file)

        # close the file
        file.close()
    except:
        data = {}
    return data



if __name__ == '__main__':
    webbrowser.open_new('http://0.0.0.0:5000/')
    app.run(host= '0.0.0.0',debug=True)
    