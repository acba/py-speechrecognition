import os
import sys
import json
import subprocess
import pyaudio

import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel

class Recognizer:

    def stream_to_text(self, stream):
        pass  

    def read_file(self, path):
        pass  


class VoskRecognizer(Recognizer):
    
    def __init__(self):

        if not os.path.exists("model"):
            print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")   
            exit(1)

        self.sample_rate=16000
        self.model = Model('model')
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def stream_to_text(self, stream, complete=False):
        dados = []

        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                resultado = json.loads(self.recognizer.Result())
                if complete:
                    dados.append(resultado)
                else:
                    dados.append(resultado['text'])

        resultado = json.loads(self.recognizer.FinalResult())
        if complete:
            dados.append(resultado)
        else:
            dados.append(resultado['text'])
            dados = ' '.join(dados)

        return dados

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

    def read_file(self, path):
        params = ['ffmpeg', '-loglevel', 'quiet', '-i', path, '-ar', str(self.sample_rate) , '-ac', '1', '-f', 's16le', '-']
        process = subprocess.Popen(params, stdout=subprocess.PIPE)
        return process.stdout


class SRRecognizer(Recognizer):

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate=22050

    def read_file(self, path):
        params = ['ffmpeg', '-loglevel', 'quiet', '-i', path, '-ar', 'str(self.sample_rate)' , '-ac', '1', '-f', 's16le', '-']
        process = subprocess.Popen(params, stdout=subprocess.PIPE)
        return process.stdout

    def to_wav(self, path):
        params = ['ffmpeg', '-loglevel', 'quiet', '-y', '-i', path, '-ar', '22050', f'{path}.wav']
        subprocess.call(params)
        return True

    def stream_to_text(self, path):
        dados = ''

        with sr.AudioFile(path) as source:
            audio = self.recognizer.record(source)

            try:
                dados = self.recognizer.recognize_google(audio, language='pt-br')
            except sr.UnknownValueError:
                dados = 'Não reconhecido'

        return dados