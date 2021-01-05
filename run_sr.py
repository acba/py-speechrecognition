import speech_recognition as sr

# Cria um reconhecedor
r = sr.Recognizer()

with sr.Microphone() as source:
    print('Escutando mic...')
    while(True):
        audio = r.listen(source)
        print(r.recognize_google(audio, language='pt-br'))