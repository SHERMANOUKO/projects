from PIL import Image

def image_converter(avatar):
    avatar = Image.open(avatar)

    # for PNG images discarding the alpha channel and fill it with some color
    if avatar.mode in ('RGBA', 'LA'):
        background = Image.new(avatar.mode[:-1], avatar.size, '#fff')
        background.paste(avatar, avatar.split()[-1])
        avatar = background
    elif avatar.mode in ('P', 'F', 'L'):
        avatar = avatar.convert('RGB')

    return avatar