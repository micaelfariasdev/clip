import shutil
import os
import glob
from gerar_video import editar
from donwload import baixar
from postar import upload
from datetime import datetime, timedelta
from utils import notify
from send import send


def automacao(
    url: str = '',
    text: str = '',
    descricao: str = '',
    hashtag: str = '',
    bg: str = '',
    inicio: str = "00:00:00",
    tempo: int = 6,
    clip: int = 2,
    down: bool = True,
    create: bool = True,
    up: bool = True
):
    """
    Automação para cortar vídeos, adicionar texto e preparar post para TikTok.

    Parâmetros:
    ----------
    url : str
        URL ou caminho do vídeo de origem.
    text : str
        Texto que será adicionado na parte superior do clipe.
    descricao : str
        Descrição do post no TikTok.
    hashtag : str
        Hashtags do post.
    inicio : str, default "00:00:00"
        Tempo inicial de corte no vídeo (formato "HH:MM:SS").
    tempo : int, default 6
        Duração total do corte em minutos (especifique na docstring).
    clip : int, default 2
        Duração de cada subclip/fatia em segundos .

    Retorna:
    -------
    None
    """
    if down:
        baixar(url, inicio=inicio, tempo=tempo)
        notify('Sucesso', 'Video Baixado com sucesso')
        print('Video Baixado com sucesso')
    if create:
        data = {
            'video': 'TEMP_CROP.mp4',
            'fonte': 'Brushot-Bold.ttf',
            'bg': bg,
            'dimensao': [720, 1280],
            'corte': clip,
            'text': f'{text}\n',
        }
        for item in glob.glob("part*"):
            if os.path.isfile(item):
                os.remove(item)
            elif os.path.isdir(item):
                shutil.rmtree(item)
        editar(data)
        notify('Sucesso', 'Clipes criado com sucesso')
        print('Clipes Criado')

    arquivos = glob.glob("part*.mp4")
    arquivos.sort(key=lambda x: int(x.split('-')[1].split('.')[0]))
    descrição_base = descricao
    hastag_lis = hashtag
    hastag_lis = hastag_lis.split()
    hastag_lis.append('#viral')
    hastag_lis.append('#fy')
    hastag_lis.append('#animetiktok')
    hastag_lis.append('#nerd')
    hastag_lis.append('#geek')
    hastag_lis.append('#FILME')
    hastag_lis.append('#lançamento')
    hastag_lis.append('#story')
    hastag_lis.append('#FYP')

    if up:
        agora = datetime.now()
        for i, arq in enumerate(arquivos):
            num = arq.split('.')[0].split('-')[1]
            descrição = f'Parte {int(num)} - {descrição_base}'
            if i == 0:
                agendado = False
            if i == 1:
                agendado_time = agora + timedelta(minutes=20)
                agendado = agendado_time.strftime("%H:%M")
            if i > 1:
                agendado_time = agendado_time + timedelta(minutes=20)
                agendado = agendado_time.strftime("%H:%M")

            upload(arq, descrição, hastag=hastag_lis,
                   agendado=agendado, headless=True)
            notify('Sucesso', f'{arq} publicado com sucesso')

    else:
        descrição = f'{descrição_base} {' '.join(hastag_lis)}'
        print(descrição)
        send(arquivos, descrição)
        notify(
            'Sucesso', f'Clipe enviado no whatsapp com sucesso')
        
    for item in glob.glob("TEMP*"):
        if os.path.isfile(item):
            os.remove(item)
        elif os.path.isdir(item):
            shutil.rmtree(item)


automacao(
    url="/home/micael-farias/Downloads/videoplayback.mp4",
    bg='https://animesonlinecc.to/wp-content/uploads/2023/08/qvgYEPOXa1eLJfkOyi5ddqK2Tmu.jpg',
    text='OnePiece Ep. 1071',
    descricao='''Luffy finalmente enfrenta Kaido! Quem vencerá?''',
    hashtag="#OnePiece #LuffyVsKaido #AnimeBattle #EpicBattle",
    inicio="00:15:20",
    tempo=2,
    clip=30,
    down=False,
    create=False,
    up=False,
)

# automacao(
#     descricao="O confronto final! Os Vingadores se unem para enfrentar Thanos e salvar o universo. Quem sairá vencedor dessa batalha épica?",
#     hashtag="#Vingadores #Thanos #Marvel #BatalhaÉpica #SuperHeróis #AvengersEndgame #MarvelFans #ClipesÉpicos #Geek #Cinema #HQ",
#     down=False,
#     create=False
# )
