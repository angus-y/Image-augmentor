import os
import random
import argparse
from PIL import Image, UnidentifiedImageError, ImageFilter


parser = argparse.ArgumentParser(description='Image processing script.')
parser.add_argument('-i', '--input', help='Input file/directory path to peform image augmentation on', required=True)
parser.add_argument("--flr", help='Perform a left right flip on the image', action="store_true")
parser.add_argument("--ftb", help='Perform a top bottom flip on the image', action="store_true")
parser.add_argument("--trs", metavar=('X','Y'), help='Perform a translation on the image displacing it along the axis by a certain number of X and Y pixels (+ve values translate left and upwards -ve values translate right and downwards)', nargs=2, type=int)
parser.add_argument("--crop", metavar=('X1','Y1','X2','Y2'), help='Perform an image crop on the bounding box : Upperleft (X1, Y1) and lower right (X2, Y2)', nargs=4, type=int)
parser.add_argument("--gau", metavar='RADIUS', help='Perform a gaussian blur transformation on the image with a specific pixel RADIUS', type=int)
parser.add_argument("--sha", metavar='ITERATIONS', help='Perform a sharpen transformation on the image for a number of ITERATIONS ', type=int)
parser.add_argument("--rot", metavar="DEGREES", help='Perform an image rotation by the specified DEGREES counter clockwise (-ve for clockwise rotation)', type=int )
parser.add_argument("--ranrot", help='Perform a counterclockwise image rotation by a certain number of degrees randomly chosen between LOWERBOUND and UPPERBOUND (-ve for clockwise rotation)',
                    metavar=("LOWERBOUND","UPPERBOUND"), nargs=2, type=int)
parser.add_argument("--fill", metavar='HEX', help='Replace any newly introduced alpha pixels with pixels of a certain HEX value during any geometric image transformation', type=str)


def flip_left_right(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def flip_top_bottom(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def rotate(image, theta, fill):
    return image.rotate(theta, fillcolor=fill)


def gaussian_blur(image, amount):
    return image.filter(ImageFilter.GaussianBlur(radius=amount))


def sharpen(image):
    return image.filter(ImageFilter.SHARPEN)


def translate(image, x, y, fill):
    return image.transform(image.size, Image.AFFINE, (1, 0, x, 0, 1, y), fillcolor=fill)


def crop(image, x1, y1, x2, y2):
    return image.crop((x1, y1, x2, y2))


def logic_handler(image, args, filename):
    fill = args.fill
    if args.flr:
        flip_left_right(image).show()
    if args.ftb:
        flip_top_bottom(image).show()
    if args.rot:
        rotate(image, args.rot, fill).show()
    if args.ranrot:
        if args.ranrot[0] < args.ranrot[1]:
            rotate(image, random.randint(args.ranrot[0], args.ranrot[1]), fill).show()
        else:
            print('[-]LOWERBOUND must be smaller than UPPERBOUND')
    if args.trs:
        translate(image, args.trs[0], args.trs[1], fill).show()
    if args.gau:
        gaussian_blur(image, args.gau).show()
    if args.sha:
        for i in range(args.sha):
            image = sharpen(image)
        image.show()
    if args.crop:
        crop(image, args.crop[0], args.crop[1], args.crop[2], args.crop[3]).show()


def main():
    args = parser.parse_args()

    if os.path.isfile(args.input):
        try:
            image = Image.open(args.input)
            logic_handler(image, args, args.input)
        except UnidentifiedImageError:
            print ("[-]Invalid image file provided")
    elif os.path.isdir(args.input): #INCOMPLETE
        os.chdir(args.input)
        for filename in os.listdir(os.getcwd()):
            try:
                image = Image.open(filename)
                logic_handler(image, args, filename)
            except UnidentifiedImageError:
                print (f"[-]Invalid image file '{i}' in provided directory")
                return
    else:
        print (f"[-]'{args.input}' is neither a valid filepath or directory path")


if __name__ == '__main__':
    main()
