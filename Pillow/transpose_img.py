from PIL import Image
from images2gif import writeGif
import random, os, imageio, time

def transpose_img(path, n):
    img = Image.open(path)
    img.convert('RGBA')
    print(img.mode)
    width, height = img.size
    img.save('./img/0.png')
    for i in range(n):
        l = random.randint(0, width - 2)
        r = random.randint(l, width - 1)
        t = random.randint(0, height -2)
        b = random.randint(t, height -1)
        box = (l, t, r, b)
        region = img.crop(box)
        region = region.transpose(Image.ROTATE_180)
        img.paste(region, box)
        img.save('./img/{}.png'.format(i + 1))

def generate_gif(dir):
    imgnames = os.listdir(dir)
    imgnames.sort()
    imglist = []
    for name in imgnames:
        img = Image.open(dir + name)
        # img.show()
        # time.sleep(0.5)
        imglist.append(img)
    imgnames.reverse()
    for name in imgnames:
        img = Image.open(dir + name)
        # img.show()
        # time.sleep(0.5)
        imglist.append(img)
    imglist.pop()
    writeGif('result.gif', imglist, duration=1, dispose=1, subRectangles=True)
    #     imglist.append(imageio.imread(dir + name))
    # imageio.imsave('./img/result.gif', imglist, 'GIF', duration=0.1)


if __name__ == '__main__':
    transpose_img('timg.jpeg', 20)
    # generate_gif('./img/')