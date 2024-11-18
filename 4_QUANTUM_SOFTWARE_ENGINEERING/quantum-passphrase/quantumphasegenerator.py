from flask import Response, request, render_template, jsonify, redirect, url_for
from braket.circuits import Circuit
from braket.aws import AwsDevice
from braket.devices.local_simulator import LocalSimulator
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

            length = int(data_recieved['size'])
            #Obtención de resultados de braket
            device = LocalSimulator()
            #device = AwsDevice()
            circuit = Circuit().h(range(length))
            braket_result = device.run(circuit, shots=100).result()
            measurement = list(braket_result.measurements[0])
            generated_string = ''.join(map(str, measurement))
            word_binary_index = []
            word = ""
            for bit in generated_string:
                if len(word) < 8:
                    word = word + bit # Concateno los bits para formar palabras de 8 bits, cada 8 bits representará un número en decimal
                else:
                    word_binary_index.append(word)
                    word = "" + bit # Iniciamos nueva palabra
            print(word_binary_index)
            #Request a data-muse
            data_muse_request = {
                'rel_jja' : 'common',
                'max' : 128
            }
            response = requests.post(DATA_MUSE_API, json=data_muse_request)
            if response.status_code == 200:
                muse_word = response.json()
                generated_phrase = ""
                for binary_index in word_binary_index:
                    # tranformación de binario a decimal
                    decimal_index = int(binary_index,2)
                    # tomo palabra del índice
                    generated_phrase = generated_phrase + muse_word[decimal_index]['word']
                return generated_phrase
    else:
        return jsonify({"error": "WRONG REQUEST"}), 400





if __name__== '__main__':
    app.run(debug=True, port=8888)