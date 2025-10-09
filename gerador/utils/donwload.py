# download_direct.py
import subprocess, shlex, sys

import subprocess
import shlex

def baixar(url, inicio, tempo, destino='gerador/download/TEMP_CROP.mp4'):
    print(f"▶️  Iniciando download e corte do vídeo...")
    print(f"    - De: {url[:50]}...") 
    print(f"    - Ponto de início: {inicio}")
    print(f"    - Duração do corte: {tempo} minuto(s)")
    print(f"    - Arquivo de destino: {destino}")
    
    h, m, s = inicio.split(':')
    h, m, s = int(h), int(m), int(s)

    m_fim = m + tempo
    if m_fim >= 60:
        h += m_fim // 60
        m_fim = m_fim % 60

    h = str(h).zfill(2)
    m_fim = str(m_fim).zfill(2)
    s = str(s).zfill(2)

    fim = ':'.join([h, m_fim, s])
    
    print(f"    - Ponto final calculado: {fim}")

    cmd = f'ffmpeg -y -hide_banner -loglevel error -i "{url}"'
    if inicio:
        cmd += f' -ss {inicio}'
    if fim:
        cmd += f' -to {fim}'

    cmd += f' -c:v copy -af "volume=0.8" "{destino}"'

    print("\n⚙️  Executando o seguinte comando com ffmpeg:")
    print(f"    {cmd}")
    print("\n⏳  Aguarde, o processo pode levar um tempo...")

    proc = subprocess.run(shlex.split(cmd))
    rc = proc.returncode
    
    if rc == 0:
        print(f"\n✅ Processo concluído com sucesso! Vídeo salvo em: '{destino}'")
    else:
        print(f"\n❌ Erro! O ffmpeg retornou o código de erro: {rc}")
        import sys
        sys.exit(rc)