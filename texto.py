from PIL import Image, ImageDraw, ImageFont


def gerar_texto(dim:list, textos:list, font_path, font_size, cor, output, stroke_width=None, stroke_color=None):
    w, h = dim
    background_path = 'image.png'
    if background_path:
        fundo = Image.open(background_path).convert("RGBA").resize((w, h))
    else:
        fundo = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    draw = ImageDraw.Draw(fundo)
    fonte = ImageFont.truetype(font_path, font_size)

    if len(textos) >= 1:
        bbox1 = draw.textbbox((0, 0), textos[0], font=fonte, stroke_width=stroke_width)
        text_w1, text_h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        x1 = (w - text_w1) // 2
        y1 = 250
        draw.text((x1, y1), textos[0], font=fonte, fill=cor,
                  stroke_width=stroke_width, stroke_fill=stroke_color)

    if len(textos) >= 2:
        bbox2 = draw.textbbox((0, 0), textos[1], font=fonte, stroke_width=stroke_width)
        text_w2, text_h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        x2 = (w - text_w2) // 2
        y2 = h - text_h2 - 250
        draw.text((x2, y2), textos[1], font=fonte, fill=cor,
                  stroke_width=stroke_width, stroke_fill=stroke_color)

    if output:
        fundo.save(output)

    return fundo


gerar_texto([720,1280],['Gay vs Madara','Part 4'], 'Brushot-Bold.ttf', 90, 'red','oi.png', 4, 'white')