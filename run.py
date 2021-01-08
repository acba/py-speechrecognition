import hashlib 
import pathlib

from flask import Flask, request, jsonify
from datetime import datetime

import ipdb

from src.recognizer import VoskRecognizer, SRRecognizer
from src.parser import TranscriptParser

app = Flask(__name__)

vosk = VoskRecognizer()
sr = SRRecognizer()


@app.route('/api/audio', methods=['POST'])
def recognize():
    if request.method == 'POST':

        file = request.files['audio_file']
        cdhash = hashlib.md5(file.stream.read()).hexdigest()
        file.seek(0)
        
        filename  = pathlib.Path(file.filename).stem
        fileext   = pathlib.Path(file.filename).suffix
        ts = datetime.timestamp(datetime.now())

        path = f'data/{filename}{fileext}'
        file.save(path)
        
        sr.to_wav(path)
        dados = sr.stream_to_text(path+'.wav')

        streama = vosk.read_file(path)
        dadosa = vosk.stream_to_text(streama)

        ret = {
            'speech_recognition': dados,
            'vosk': dadosa
        }

        return jsonify(ret)
    else:
        return 'Error'
