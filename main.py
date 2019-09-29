from termcolor import colored
from PIL import Image
import numpy as np
import sys

class Renderer():

    def __init__(self):
        self.cols = [
            ('black', np.array([[0, 0, 0]]), []),
            ('red',  np.array([[255, 50, 50]]), []),
            ('green',  np.array([[50, 255, 50]]), []),
            ('yellow',  np.array([[255, 255, 50]]), []),
            ('blue',  np.array([[50, 50, 255]]), []),
            ('magenta',  np.array([[255, 50, 255]]), []),
            ('cyan',  np.array([[50, 255, 255]]), []),
            ('red',  np.array([[255, 150, 150]]), ['blink']),
            ('green',  np.array([[150, 255, 150]]), ['blink']),
            ('yellow',  np.array([[255, 255, 150]]), ['blink']),
            ('blue',  np.array([[150, 150, 255]]), ['blink']),
            ('magenta',  np.array([[255, 150, 255]]), ['blink']),
            ('cyan',  np.array([[150, 255, 255]]), ['blink']),
            ('white',  np.array([[255, 255, 255]]), []),
        ]

    def get_pixel(self, color):
        # compute cosine similatiry against colour for all available cols
        # generate coloured pixel using best available colour
        col = sorted(self.cols, key=lambda x: np.linalg.norm( x[1] - color.reshape(1, -1) ))[0]
        if col[0] == 'black':
            return '  '
        return colored('  ', col[0], f'on_{col[0]}', attrs=col[2])

    def render_image(self, pixels, scale):
        # first of all scale the image to the scale 'tuple'
        image_size = pixels.shape[:2]
        block_size = (image_size[0]/scale[0], image_size[1]/scale[1])
        blocks = []
        y = 0
        while y < image_size[0]:
            x = 0
            block_col = []
            while x < image_size[1]:
                # get a block, reshape in into an Nx3 matrix and then get average of each column
                block_col.append(pixels[int(y):int(y+block_size[0]), int(x):int(x+block_size[1])].reshape(-1, 3).mean(axis=0))
                x += block_size[1]
            blocks.append(block_col)
            y += block_size[0]
        output = [[self.get_pixel(block) for block in row] for row in blocks]
        return output
        
        


def get_image(path):
    img = np.asarray(Image.open(path))
    if img.shape[2] > 3:
        return np.array([[pixel[:3] for pixel in row] for row in img])
    return img

def main():
    renderer = Renderer()
    path = sys.argv[1]
    image = get_image(path)
    output = renderer.render_image(image, (60, 60))
    print('\n'.join([''.join(row) for row in output]))

if __name__ == '__main__':
    main()
