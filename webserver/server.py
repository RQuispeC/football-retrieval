import os, glob, errno

import sys
sys.path.insert(0, '../')

from functools import wraps
from flask import Flask, render_template, request, redirect, Response,jsonify
import random, json
from flask_cors import CORS, cross_origin

import requests

from football_lib.match import Match
from football_lib.interface.draw import plot_position, plot_comparison, generate_video


import matplotlib.pyplot as plt



app = Flask(__name__)
cors = CORS(app, resources={r"/receiver": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def output():
    # serve index template
    return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
@app.route('/receiver/<value>/<value2>', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def worker(value,value2):
    cars = ["Volvo","Ferrari","Audi","BMW","Mercedes","Porche","Saab","Avanti"]
    name = {}
    #i=0
    #for value in cars:
    name['values'] = cars
    #    i = i+1
    #return name
    return json.dumps(name)

@app.route('/player', methods = ['POST'])
@app.route('/player/<str_>/<val>/<mat1>/<mat2>/<rep>/<player>/<team>/<ratio>/<dis>', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def player(str_,val,mat1,mat2,rep,player,team,ratio,dis):
    print(str_)
    print(val)
    print(mat1)
    print(rep,player,team,ratio,dis)
    name = {}
    #i=0
    #for value in cars:
    name['sucesso'] = "sucesso"
    #    i = i+1
    #return name
    return json.dumps(name)

@app.route('/team', methods = ['POST'])
@app.route('/team/<str_>/<val>/<mat1>/<mat2>/<team>/<ratio>/<dis>', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def team(str_,val,mat1,mat2,team,ratio,dis):
    print(str_)
    print(val)
    print(mat1)
    print(team,ratio,dis)
    name = {}
    #i=0
    #for value in cars:
    name['sucesso'] = "sucesso"
    #    i = i+1
    #return name
    return json.dumps(name)


@app.route('/tamanho_g', methods = ['POST'])
@app.route('/tamanho_g/<j1>/<j2>', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def tamanho_g(j1,j2):
	f1 = open('../data/Dados Futebol/'+j1+".2d",'r')
	f2 = open('../data/Dados Futebol/'+j2+".2d",'r')
	num_lines1 = sum(1 for line in f1)
	num_lines2 = sum(1 for line in f2)

	ret = {}
	ret['qtd1'] = num_lines1
	ret['qtd2'] = num_lines2

	return json.dumps(ret)


@app.route('/visualize', methods = ['POST'])
@app.route('/visualize/<pos>/<str_>/<val>/<mat1>/<mat2>/<team>', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def visualize(pos,str_,val,mat1,mat2,team):
    if(team == 0):
        fpath = '../data/Dados Futebol/'+mat1+".2d"
    else:
        fpath = '../data/Dados Futebol/'+mat2+".2d"

    print(fpath)
    fpath = "/home/leodecio/workspace/football-retrieval/data/Dados Futebol/CapBotT1Suav.2d"
    match = Match(fpath, edge_strategy_name=str_, graph_representation_name = 'embedding', thr = val)
    plot_position(match[pos],'out_data/')

    name = {}
    #i=0
    #for value in cars:
    name['path'] = "../webserver/out_data/"+str(pos)+".png"
    #    i = i+1
    #return name
    return json.dumps(name)



def getImageUrl(diretorio_usuario, diretorio, dicionario):
    if os.path.isdir(diretorio_usuario + diretorio):
        os.chdir(diretorio_usuario + diretorio)
        for arquivo in glob.glob("*"):
            if((arquivo).endswith(".2d")):# or (arquivo).endswith(".png") or (arquivo).endswith(".jpeg")):
                #dicionario[diretorio_usuario+diretorio+arquivo] = []
                dicionario[arquivo[:-3]] = []
                dicionario[arquivo[:-3]].append(arquivo[:-7])
    return dicionario


@app.route('/games', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def games():
    current = os.getcwd()

    diretorio_usuario = "../data/"
    diretorio = "Dados Futebol/"
    dicionario = {}


    d = getImageUrl(diretorio_usuario,diretorio,dicionario)
    os.chdir(current)
    
    return json.dumps(d)

@app.route('/video', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def video():
    
    d = {"url":"../webapp/data/video.mp4"}

    return json.dumps(d)

if __name__ == '__main__':
    # run!
    app.run()