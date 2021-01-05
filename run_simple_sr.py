import sys
import speech_recognition as sr

AUDIO_FILE = sys.argv[1]

# Cria um reconhecedor
r = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
    print('Escutando arquivo...')
    audio = r.record(source)

    try:
        print(r.recognize_google(audio, language='pt-br'))
    except sr.UnknownValueError:
        print('O google não conseguiu reconhecer pica nenhuma')