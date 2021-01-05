from src.transcricao import Transcricao

tr = Transcricao()
texto = tr.mic_to_text()

print(texto)