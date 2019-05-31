import os, glob, errno

import sys
from functools import wraps
from flask import Flask, render_template, request, redirect, Response,jsonify
import random, json
from flask_cors import CORS, cross_origin

import requests



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

def getImageUrl(diretorio_usuario, diretorio, dicionario):
    if os.path.isdir(diretorio_usuario + diretorio):
        os.chdir(diretorio_usuario + diretorio)
        for arquivo in glob.glob("*"):
            if((arquivo).endswith(".2d")):# or (arquivo).endswith(".png") or (arquivo).endswith(".jpeg")):
                dicionario[diretorio_usuario+diretorio+arquivo] = []
                dicionario[diretorio_usuario+diretorio+arquivo].append(arquivo[:-7])
    return dicionario


@app.route('/games', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@support_jsonp
def games():
    current = os.getcwd()

    diretorio_usuario = "/home/leodecio/Área de Trabalho/Unicamp/1st_semester/recuperacao_de_informacao/pesquisa/"
    diretorio = "Dados Futebol/"
    dicionario = {}

    d = getImageUrl(diretorio_usuario,diretorio,dicionario)
    os.chdir(current)
    
    return json.dumps(d)

if __name__ == '__main__':
    # run!
    app.run()