from PIL import Image, ImageDraw, ImageFont
import tempfile

async def title_card(message, client):
    height = 720
    width = 2000
    img = Image.new('RGBA', (width, height), (0,0,0,255))
    sz = 100
    fnt = ImageFont.truetype('/usr/share/fonts/textile-regular.ttf', sz)
    txt = Image.new('RGBA', img.size, (255,255,255,0))
    d = ImageDraw.Draw(txt)
    
    c = message.content.split(' ')
    current_string = c[0]
    current_strings = []
    for (idx,w) in enumerate(c):
        if idx == 0:
            continue
        if (len(current_string) + 1 + len(w)) * sz > width:
            current_strings.append(current_string)
            current_string = w
        else:
            current_string += ' ' + w
    
    if current_string != '':
        current_strings.append(current_string)

    for (idx,string) in enumerate(current_strings):
        d.text( (width/2 - len(string)*sz/4, height/2 - len(current_strings)*sz/2 + idx*(sz+10)), string, font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(img, txt)
    tmpfile = tempfile.NamedTemporaryFile(suffix='.png')
    out.save(tmpfile.name)
    with open(tmpfile.name, 'r+b') as f:
        await client.send_file(message.channel, f)
