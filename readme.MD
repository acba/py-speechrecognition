# py-speechrecognition

Fram

## Requisitos
* Transcrever arquivos de audio com marcações temporais
* Gerar nuvem de palavras e estatisticas


## Ajuda

### Filtro FFmpeg

### Model information

The following table maps expected signal (horizontal) against expected noise
(vertical). Note that "voice" is distinct from "speech" by the presence of
non-speech human sounds, such as laughter.

|                   | General               | Voice                 | Speech                |
| ----------------- | --------------------- | --------------------- | --------------------- |
| General           | marathon-prescription | leavened-quisling     | orig                  |
| Recording         | conjoined-burgers     | beguiling-drafter     | somnolent-hogwash     |

Modelos capturados em https://github.com/GregorR/rnnoise-models

`
    $ ffmpeg -i $INPUT -af 'arnndn=m=filter/bd.rnnn' $OUTPUT
    $ ffmpeg -i $INPUT -af 'arnndn=m=filter/lq.rnnn' $OUTPUT
`

## dependencias

sudo apt install swig portaudio19-dev


