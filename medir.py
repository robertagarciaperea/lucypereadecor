import os
from PIL import Image
for f in sorted(os.listdir('out')):
    im = Image.open('out/' + f); print(f, im.size)
    im.thumbnail((400, 400)); im.save('out/' + f)
