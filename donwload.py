# download_direct.py
import subprocess, shlex, sys

def baixar(url, inicio, tempo, destino='TEMP_CROP.mp4'):
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
    print(fim)
    cmd = f'ffmpeg -y -hide_banner -loglevel error -i "{url}"'
    if inicio:
        cmd += f' -ss {inicio}'
    if fim:
        cmd += f' -to {fim}'
    cmd += f' -c copy "{destino}"'
    proc = subprocess.run(shlex.split(cmd))
    rc = proc.returncode
    if rc == 0:
        print("Concluído:", destino)
    else:
        print("Erro, código:", rc)
        sys.exit(rc)

