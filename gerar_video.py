# Importa as classes necessárias do moviepy
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, vfx, ImageClip
from texto import gerar_texto
import numpy as np

def editar_video_com_texto(n):
    """
    """
    video_path = f"parte_0{str(n).zfill(2)}.mp4"
    font_path = "Brushot-Bold.ttf"
    output_path = f"part{str(n).zfill(2)}.mp4"


    print(f"Carregando vídeo de: {video_path}")
    clip = VideoFileClip(video_path)

    target_width = 720
    target_height = 1280

    print(
        f"Redimensionando o vídeo para {target_width}x{target_height}...")
    clip_redimensionado = clip.with_effects(
        [vfx.Resize(width=target_width)])


    print("Criando o clipe de texto...")
    # Gera a imagem do texto (retorna PIL.Image)
    img_texto = gerar_texto(
        [target_width, target_height],
        ['Gai vs Madara', f'Part {n}'],
        'Brushot-Bold.ttf',
        90,
        'red',
        output=None,  
        stroke_width=4,
        stroke_color='white'
    )
    frame = np.array(img_texto)

    # Converte para ImageClip
    back = ImageClip(frame).with_duration(clip.duration)


    print("Combinando vídeo e texto...")
    video_final = CompositeVideoClip([back, clip_redimensionado.with_position("center")])

    print(f"Gerando o arquivo final: {output_path}...")
    video_final.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    preset="ultrafast",
    ffmpeg_params=["-tune", "fastdecode", "-crf", "28"]
)


    print(
        f"\nEdição concluída com sucesso! O vídeo foi salvo como '{output_path}'.")




from multiprocessing import Pool

if __name__ == "__main__":
    with Pool(1) as p:  # 4 processos em paralelo
        p.map(editar_video_com_texto, range(6, 11))
