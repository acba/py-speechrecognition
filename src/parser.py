
class TranscriptParser:

    def __init__(self):
        pass

    def extract_text(self, dados):
        text = ''

        for dado in dados:
            text += dado['text'] + ' '

        return text.strip()

    def find(self, dados, termo):
        result = []

        for dado in dados:
            for r in dado['result']:
                if termo in r['word']:
                    result.append(r)

        return result