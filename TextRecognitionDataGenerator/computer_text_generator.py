import random

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

def generate(text, font, text_color, font_size, orientation, space_width, fit):
    if orientation == 0:
        return _generate_horizontal_text(text, font, text_color, font_size, space_width, fit)
    elif orientation == 1:
        return _generate_vertical_text(text, font, text_color, font_size, space_width, fit)
    else:
        raise ValueError("Unknown orientation " + str(orientation))

def _generate_horizontal_text(text, font, text_color, font_size, space_width, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)
    words = text.split(' ')
    
    for i,e in enumerate(words):
        words[i] = e + " "
        
    space_width = image_font.getsize(' ')[0] * space_width

    words_width = [image_font.getsize(w)[0] for w in words]
    text_width =  sum(words_width) + int(space_width) * (len(words) - 1)
    text_height = max([image_font.getmask(w).size[1] for w in words])
    text_height = int(text_height * 2)
    txt_img = Image.new('RGBA', (text_width, text_height + 500), (0,0,0,0))

    # print(txt_img.size, text_height, text_width)
    txt_draw = ImageDraw.Draw(txt_img)
    
    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
    c1, c2 = colors[0], colors[-1]

    fill = (
        random.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        random.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        random.randint(min(c1[2], c2[2]), max(c1[2], c2[2]))
    )

    for i, w in enumerate(words):
        txt_draw.text((sum(words_width[0:i]) + i * int(space_width), 100), w, fill=fill, font=image_font,language="th")
        # print((sum(words_width[0:i]) + i * int(space_width), 1))
    # txt_img.show()
    if fit:
        # print("txt_img.getbbox()",txt_img.getbbox())
        # newMargin =  txt_img.getbbox()
        # newMargin = ((newMargin[0]/100)*90,newMargin[1],(newMargin[2]/100)*90,newMargin[3])
        # return txt_img.crop(newMargin)
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img

def _generate_vertical_text(text, font, text_color, font_size, space_width, fit):
    image_font = ImageFont.truetype(font=font, size=font_size)
    
    space_height = int(image_font.getsize(' ')[1] * space_width)

    char_heights = [image_font.getsize(c)[1] if c != ' ' else space_height for c in text]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights)
    
    txt_img = Image.new('RGBA', (text_width, text_height), (0,0,0,0))
    
    txt_draw = ImageDraw.Draw(txt_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
    c1, c2 = colors[0], colors[-1]

    fill = (
        random.randint(c1[0], c2[0]),
        random.randint(c1[1], c2[1]),
        random.randint(c1[2], c2[2])
    )

    for i, c in enumerate(text):
        txt_draw.text((0, sum(char_heights[0:i])), c, fill=fill, font=image_font)

    if fit:
        return txt_img.crop(txt_img.getbbox())
    else:
        return txt_img
