import os
import sys
import json
import subprocess
import pyaudio

from vosk import Model, KaldiRecognizer, SetLogLevel

class Transcricao:
    def __init__(self):

        if not os.path.exists("model"):
            print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")   
            exit(1)

        self.sample_rate=16000
        self.model = Model('model')
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def stream_to_text(self, stream):
        transcricao = []
        dados = []

        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                resultado = self.recognizer.Result()
                transcricao.append(json.loads(resultado)['text'])
                dados.append(json.loads(resultado))


        resultado = self.recognizer.FinalResult()
        transcricao.append(json.loads(resultado)['text'])
        dados.append(json.loads(resultado))

    def mic_to_text(self):
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        texto_transcrito = []
        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                resultado = self.recognizer.Result()
                parcial = json.loads(resultado)['text']
                
                if parcial != '':
                    texto_transcrito.append(parcial)
                    print(parcial)

                if parcial == 'fechar' or parcial == 'fim':
                    break


        resultado = self.recognizer.FinalResult()
        texto_transcrito.append(json.loads(resultado)['text'])

        return texto_transcrito


    def file_to_stream(self, path):
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', path, '-ar', str(self.sample_rate) , '-ac', '1', '-f', 's16le', '-'], stdout=subprocess.PIPE)
        return process.stdout
