from moviepy import VideoFileClip, CompositeVideoClip, vfx, ImageClip
import requests
from io import BytesIO
from .utils import notify
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from tqdm import tqdm
import subprocess, shlex

def gerar_texto(dim: list, textos: list, font_path, font_size, cor, output, stroke_width=None, stroke_color=None, background_path=None):
    w, h = dim
    if background_path:
        if background_path.startswith('http'):
            response = requests.get(background_path)
            img = BytesIO(response.content)
        else:
            img = background_path
        fundo = Image.open(img).convert("RGBA").resize((w, h))
    else:
        fundo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fundo = ImageEnhance.Brightness(fundo).enhance(0.5)
    fundo = fundo.filter(ImageFilter.GaussianBlur(5))
    draw = ImageDraw.Draw(fundo)

    for i, texto in enumerate(textos):
        tamanho_atual = font_size
        fonte = ImageFont.truetype(font_path, tamanho_atual)
        bbox = draw.textbbox((0,0), texto, font=fonte, stroke_width=stroke_width)
        text_w = bbox[2] - bbox[0]

        while text_w > w * 0.9 and tamanho_atual > 5:
            tamanho_atual -= 1
            fonte = ImageFont.truetype(font_path, tamanho_atual)
            bbox = draw.textbbox((0,0), texto, font=fonte, stroke_width=stroke_width)
            text_w = bbox[2] - bbox[0]

        x = (w - text_w) // 2
        y = 250 if i == 0 else h - (bbox[3]-bbox[1]) - 250

        draw.text((x, y), texto, font=fonte, fill=cor, stroke_width=stroke_width, stroke_fill=stroke_color)

    if output:
        fundo.save(output)

    return fundo

def cortar(arq, inicio, fim):
    cmd = f'ffmpeg -y -hide_banner -loglevel error -i "{arq}"'
    if inicio:
        cmd += f' -ss {inicio}'
    if fim:
        cmd += f' -to {fim}'
    cmd += f' -c copy "gerador/download/TEMP_CROP_PART.mp4"'
    proc = subprocess.run(shlex.split(cmd))
    return "gerador/download/TEMP_CROP_PART.mp4"

def editar(n):
    """
    """
    video_path = n['video']
    init = "00:00:00"
    h, m, s = init.split(':')
    h, m, s = int(h), int(m), int(s)

    s_fim = s + n['corte']
    if s_fim >= 60:
        m += s_fim // 60
        s_fim = s_fim % 60

    h = str(h).zfill(2)
    m = str(m).zfill(2)
    s_fim = str(s_fim).zfill(2)
    final = ':'.join([h, m, s_fim])


    clip = VideoFileClip(video_path)
    for_num = int(clip.duration / (n['corte']))
    target_width, target_height = n['dimensao']
    
    print(f"🎬 Vídeo será dividido em {for_num} partes de {n['corte']} segundos cada.")
    
    for part in range(1, int(for_num) + 1):
        print(f"\n--- 🎞️ Processando Parte {part}/{int(for_num)} ---")
        
        output_path = f"parte-{str(part).zfill(2)}.mp4"
        
        print(f"  [1/3] ✂️  Cortando trecho do vídeo de {init} a {final}...")
        video_path_crop = cortar(video_path,init,final)
        
        clip = VideoFileClip(video_path_crop)
        clip_redimensionado = clip.with_effects(
            [vfx.Resize(height=600)])
        
        print(f"  [2/3] ✍️  Gerando imagem de texto sobreposta...")
        img_texto = gerar_texto(
            [target_width, target_height],
            [n['text'], f'Parte {part}'],
            n['fonte'],
            90,
            'red',
            output=None,
            stroke_width=4,
            stroke_color='white',
            background_path=n['bg']
        )

        frame = np.array(img_texto)
        back = ImageClip(frame).with_duration(clip.duration)
        video_final = CompositeVideoClip(
            [back, clip_redimensionado.with_position("center")])

        print(f"  [3/3] 🚀 Renderizando vídeo final para '{output_path}'...")

        video_final.write_videofile(
            output_path,
            fps=28,
            codec="libx264",
            preset="ultrafast",
            threads=8,
            audio_codec="aac",
            ffmpeg_params=["-tune", "fastdecode", "-crf", "32"], 
            # logger=None, # Mantemos None aqui para não ter duas barras
        )
        print(f"  ✨ Parte {part} concluída!")
        notify('Sucesso', f'Parte {part} concluída!')

        init = final
        h, m, s = init.split(':')
        h, m, s = int(h), int(m), int(s)

        s_fim = s + n['corte']
        if s_fim >= 60:
            m += s_fim // 60
            s_fim = s_fim % 60

        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s_fim = str(s_fim).zfill(2)
        final = ':'.join([h, m, s_fim])
    
    return print(f"\n✅ Processo finalizado! A última parte criada foi '{output_path}'.")