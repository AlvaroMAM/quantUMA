"""
Alumno: Álvaro Manuel Aparicio Morales
I CERTIFICADO DE EXTENSIÓN UNIVERSITARIA EN COMPUTACIÓN CUÁNTICA 
Curso : 2024-25
Módulo 4 - Software Cuántico
"""

from flask import Flask, Response, request, render_template, jsonify, redirect, url_for
import json
import requests


app = Flask(__name__)

SERVER_URL = "http://127.0.0.1:8888/"

@app.route('/')
def index ():
    return render_template('home.html')


@app.route('/')
def alive ():
    return Response("It's alive")

@app.route ('/quantumphasegenerator', methods=['POST'])
def quantumphasegenerator():
    results = None
    if request.method == 'POST':
        length = request.form['size']
        data = {'length' : length}
        response = requests.post(SERVER_URL+"generate-random-bits", json=data)
        print("PETICION HECHA")
        if response.status_code == 200:
            results  = response.json()
            return render_template('home.html', resultado=results["result"])
        else:
            return Response("Something was wrong during request to server")
    else: 
        return Response("Wrong petition")



if __name__== '__main__':
    app.run(debug=True, port=5555)