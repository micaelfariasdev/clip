import shutil
import os
import glob
from .utils import editar, baixar, upload, notify, send
from datetime import datetime, timedelta


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
    up: bool = True,
    send_: bool = True,
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
            'video': 'gerador/download/TEMP_CROP.mp4',
            'fonte': 'gerador/utils/Brushot-Bold.ttf',
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

    if send_:
        descrição = f'{descrição_base} {' '.join(hastag_lis)}'
        print(descrição)
        send(arquivos, descrição)
        notify(
            'Sucesso', f'Clipe enviado no whatsapp com sucesso')
        
    print("🧹 Procurando por arquivos e pastas temporárias (TEMP*) para limpar...")

    # Define o diretório de busca para ser reutilizado
    
    print(f"🔍 arquvios: {glob.glob("**/TEMP*", recursive=True)}")
    # Usa o glob para encontrar os itens
    for item_name in glob.glob("**/TEMP*", recursive=True):
        
        # Constrói o caminho completo para o item encontrado
        full_path = os.path.join(item_name)

        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
                print(f"  🗑️ Arquivo removido: {full_path}")
            
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
                print(f"  🗑️ Diretório removido: {full_path}")
        
        except OSError as e:
            print(f"  ❌ Erro ao remover {full_path}: {e}")

    print("✅ Limpeza concluída.")



