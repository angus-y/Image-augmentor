import os
import sys
from PIL import Image


def resize_image(file_path):
    im = Image.open(file_path)
    if im.size[0] > 512 and im.size[1] > 512:
        cropped_im = im.crop((0,0,512,512))
    else:
        cropped_im = im.resize((512,512))
    return cropped_im


def main(folder_dir):
    os.chdir(folder_dir)
    for i in os.listdir(os.getcwd()):
        print (f'[*]Resizing {i}')
        fname = os.path.splitext(i)[0]
        extension = os.path.splitext(i)[1]
        save_dir = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        resize_image(i).save(os.path.join(save_dir, fname + '_cropped' + extension))


if __name__ == '__main__':
    main(sys.argv[1])
