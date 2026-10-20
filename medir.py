import os
from PIL import Image
for f in sorted(os.listdir('out')):
    if not f.endswith('.png'): continue
    try:
        im = Image.open('out/' + f); print(f, im.size)
    except Exception as e:
        print(f, 'ERR', e); continue
    im.thumbnail((400, 400)); im.save('out/' + f)
