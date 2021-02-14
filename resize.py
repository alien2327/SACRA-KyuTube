from PIL import Image
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

parent = "./kyu_img/"
img_list = os.listdir(parent)
for img in img_list:
    size = os.path.getsize(parent+img)
    if size > 3000000:
        PIL_img = Image.open(parent+img)
        img_resize = PIL_img.resize((int(PIL_img.width / 2), int(PIL_img.height / 2)))
        img_resize.save(parent+img[:-4]+"_resized.jpg")
