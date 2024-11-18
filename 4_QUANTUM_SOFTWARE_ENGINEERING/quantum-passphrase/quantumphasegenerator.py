from flask import Response, request, render_template, jsonify, redirect, url_for
import json
import requests


app = Flask(__name__)

CLIENT_URL = http://127.0.0.1:5555

DATA_MUSE_API = "https://api.datamuse.com/words"

@app.route('/')
def alive ():
    return Response("It's alive")

@app.route('/quantumphasegenerator', method=['POST'])
def quantumphasegenerator():

    if request.method == 'POST':
        data_recieved = request.get_json()
    
        if not data_recieved or 'size' not in data_recieved:
            return jsonify({"error": "Falta el parámetro 'size' en el cuerpo de la solicitud"}), 400
        else:
            length = data_recieved['size']

            # Construcción de algoritmo cuántico y lanzamiento a braket
                # Bucle para añadir puertas hadamard
            #Obtención de resultados de braket
            braket_result = None
            #Request a data-muse
            data_muse_request = {
                'rel_jja' : 'common',
                'max' : braket_result
            }
            response = requests.post(DATA_MUSE_API, json=data_muse_request)
            if response.status_code == 200:
                words  = [word['word'] for word in response.json()]
                return words
    else:
        return jsonify({"error": "WRONG REQUEST"}), 400





if __name__== '__main__':
    app.run(debug=True, port=8888)