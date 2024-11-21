"""
Alumno: Álvaro Manuel Aparicio Morales
I CERTIFICADO DE EXTENSIÓN UNIVERSITARIA EN COMPUTACIÓN CUÁNTICA 
Curso : 2024-25
Módulo 4 - Software Cuántico
"""

from flask import Flask, Response, request, render_template, jsonify, redirect, url_for
from braket.circuits import Circuit
from braket.devices.local_simulator import LocalSimulator
import json
import requests

app = Flask(__name__)

CLIENT_URL = "http://127.0.0.1:5555"

DATA_MUSE_API = "https://api.datamuse.com/words"

@app.route('/')
def alive ():
    return Response("It's alive")

@app.route('/generate-random-bits', methods=['POST'])
def quantumphasegenerator():
    print("LLEGA PETICION AL SERVER")
    if request.method == 'POST':
        print("ES POST")
        data_recieved = request.get_json()
        print(data_recieved)
        if not data_recieved or 'length' not in data_recieved:
            return jsonify({"error": "Length missing"}), 400
        else:
            
            length = int(data_recieved['length'])
            device = LocalSimulator()
            circuit = Circuit().h(range(length))
            braket_result = device.run(circuit, shots=100).result()
            measurement = list(braket_result.measurements[0])
            generated_string = ''.join(map(str, measurement))
            print(generated_string)
            word_binary_index = []
            word = ""
            for bit in generated_string:
                if len(word) < 8:
                    word = word + bit # Concateno los bits para formar palabras de 8 bits, cada 8 bits representará un número en decimal
                else:
                    word_binary_index.append(word)
                    word = "" + bit # Iniciamos nueva palabra
            word_binary_index.append(word) # Añadimos el residuo
            #Request a data-muse
            params = {
                'rel_jja' : 'common',
                'max' : 256
            }
            response = requests.get(DATA_MUSE_API, params=params)
            if response.status_code == 200:
                print("DATA MUSE WORDS")
                muse_words = response.json()
                print(len(muse_words))
                print(muse_words)
                generated_phrase = ""
                for binary_index in word_binary_index:
                    # tranformación de binario a decimal
                    decimal_index = int(binary_index,2)
                    if decimal_index >=len(muse_words):
                        decimal_index = decimal_index % len(muse_words)
                    # tomo palabra del índice
                    print(decimal_index)
                    muse_word = muse_words[decimal_index]
                    print(muse_word)
                    generated_phrase = generated_phrase + " " + muse_word['word']
                print(generated_phrase)
                return jsonify({"result" : generated_phrase})
            else:
                print(response.json())
                return jsonify({"error": "DATA MUSE PROBLEM"}), 400
    else:
        return jsonify({"error": "WRONG REQUEST"}), 400





if __name__== '__main__':
    app.run(debug=True, port=8888)