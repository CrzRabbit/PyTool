from PIL import Image
from images2gif import writeGif
import random, os, imageio, time

def transpose_img(path, n):
    try:
        img = Image.open(path)
    except IOError:
        img = Image.new('RGB', (500, 500), (255, 255, 255))
    img.convert('RGBA')
    width, height = img.size
    img.save('./img/0.png')
    for i in range(n):
        l = random.randint(0, width - 21)
        r = random.randint(l + 20, width - 1)
        t = random.randint(0, height -21)
        b = random.randint(t + 20, height -1)
        box = (l, t, r, b)
        region0 = img.crop(box)
        region0 = region0.transpose(Image.ROTATE_180)
        rgb_r = random.randint(100, 255)
        rgb_g = random.randint(0, 50)
        rgb_b = random.randint(0, 50)
        # a = random.randint(0, 255)
        region = Image.new('RGB', (r - l, b - t), (rgb_r, rgb_g, rgb_b))
        img.paste(Image.blend(region, region0, 0.1), box)
        # img.paste(region, box)
        img.save('./img/{}.png'.format(i + 1))
    img.show()

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
    pass
    # transpose_img('timg.jpeg', 100)
    # generate_gif('./img/')