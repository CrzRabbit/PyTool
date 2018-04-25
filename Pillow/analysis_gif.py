from PIL import Image
import os, imageio

def analysis_tile(path):
    img = Image.open(path)

    results = {
        'size': img.size,
        'mode': None}

    try:
        while True:
            if img.tile:
                tile = img.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != img.size:
                    results['mode'] = 'partial'
                    break
                img.seek(img.tell() + 1)
                print('tile of img: {0} {1} {2}'.format(tile, update_region, update_region_dimensions))
    except EOFError:
        pass
    print('results: {}'.format(results))
    return results

def analysis_gif(path):

    mode = analysis_img(path)['mode']

    i = 0
    img = Image.open(path)
    p = img.getpalette()
    last_frame = img.convert('RGBA')
    try:
        while True:
            if not img.getpalette():
                img.putpalette(p)

            new_frame = Image.new('RGBA', img.size)

            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(img, (0, 0), img.convert('RGBA'))
            new_frame.save('img/ag_{}.png'.format(i), 'PNG')

            i += 1
            last_frame = new_frame
            img.seek(img.tell() + 1)
    except EOFError:
        pass

def generate_gif(path, gname):
    names = os.listdir(path)
    names.sort()

    frames = []
    for name in names:
        if 'png' == name.split('.')[1]:
            frames.append(imageio.imread(path + name))

    try:
        imageio.mimsave(gname, frames, 'GIF', duration=0.1)
    except RuntimeError:
        pass

if __name__ == '__main__':
    analysis_gif('hug.gif')
    generate_gif('img/', 'result.gif')