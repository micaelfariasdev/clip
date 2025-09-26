import shutil
import os
import glob
from gerar_video import editar
from donwload import baixar
from postar import upload
from datetime import datetime, timedelta

baixar("https://p1.animescomix.com/stream/animes-dublado/n/naruto-dublado/133.mp4",
       inicio="00:08:50", tempo=6)

data = {
    'video': 'TEMP_CROP.mp4',
    'fonte': 'Brushot-Bold.ttf',
    'bg': 'image.png',
    'dimensao': [720, 1280],
    'corte': 2,
    'text': 'Superman\n',
}

editar(data)

arquivos = glob.glob("part*.mp4")
print(arquivos)

descrição = 'askjdnaskdn'
hastag = '#asadasd'
tempo = datetime.now()
for i, arq in enumerate(arquivos):
    if i == 0:
        agendado = False
    if i >= 1:
        tempo = tempo + timedelta(minutes=20)
        agendado = tempo.strftime("%H:%M")
    upload(arq, descrição, agendado=agendado)

for item in glob.glob("TEMP*"):
    if os.path.isfile(item):
        os.remove(item)
    elif os.path.isdir(item):
        shutil.rmtree(item)
