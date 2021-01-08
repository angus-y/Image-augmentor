import os
import random
import argparse
from datetime import datetime
from PIL import Image, UnidentifiedImageError, ImageFilter


parser = argparse.ArgumentParser(description='Image processing script.')
parser.add_argument('-i', '--input', help='Input file/directory path to peform image augmentation on', required=True)
parser.add_argument('-r', '--repeat', help='Number of times to repeat image augmentations', action="store_true")
parser.add_argument('-s', '--source', help='Process only source files, ignore files that end with the augment identifiers (e.g. ignore: file_flr.png, file_ftb (2).png)', action="store_true")
parser.add_argument("--flr", help='Perform a left right flip on the image', action="store_true")
parser.add_argument("--ftb", help='Perform a top bottom flip on the image', action="store_true")
parser.add_argument("--trs", metavar=('X','Y'), help='Perform a translation on the image displacing it along the axis by a certain number of X and Y pixels (+ve values translate left and upwards -ve values translate right and downwards)', nargs=2, type=int)
parser.add_argument("--crop", metavar=('X1','Y1','X2','Y2'), help='Perform an image crop on the bounding box : Upperleft (X1, Y1) and lower right (X2, Y2)', nargs=4, type=int)
parser.add_argument("--rancrop", metavar=('WIDTH', 'HEIGHT'), help='Perform a random image crop to create an image of specific WIDTH and HEIGHT', nargs=2, type=int)
parser.add_argument("--gau", metavar='RADIUS', help='Perform a gaussian blur transformation on the image with a specific pixel RADIUS', type=int)
parser.add_argument("--rangau", metavar=("LOWERBOUND","UPPERBOUND"), help='Perform a gaussian blur transformation on the image with a specific pixel radius randomly chosen between LOWERBOUND and UPPERBOUND', nargs=2, type=int)
parser.add_argument("--sha", metavar='ITERATIONS', help='Perform a sharpen transformation on the image for a number of ITERATIONS', type=int)
parser.add_argument("--ransha", metavar=("LOWERBOUND","UPPERBOUND"), help='Perform a sharpen transformation on the image for a number of iterations randomly chosen between LOWERBOUND and UPPERBOUND', nargs=2, type=int)
parser.add_argument("--rot", metavar="DEGREES", help='Perform an image rotation by the specified DEGREES counter clockwise (-ve for clockwise rotation)', type=int)
parser.add_argument("--ranrot", help='Perform a counterclockwise image rotation by a certain number of degrees randomly chosen between LOWERBOUND and UPPERBOUND (-ve for clockwise rotation)',
                    metavar=("LOWERBOUND","UPPERBOUND"), nargs=2, type=int)
parser.add_argument("--gnoi", metavar=("AMOUNT", "ALPHA"), help='Add a certain AMOUNT of gaussian noise to the image blended with a certain ALPHA (between 0 and 1)', nargs=2, type=float)
parser.add_argument("--rangnoi", metavar=("LOWERBOUND", "UPPERBOUND", "ALPHA"), help='Add a certain amount of gaussian noise to the image randomly chosen between LOWERBOUND and UPPERBOUND of a certain ALPHA', nargs=3, type=float)
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


def save_file(image, file_attr, transformation, current_dir):
    filename = file_attr[0] + transformation + file_attr[1]
    if filename in current_dir:
        copy = 1
        filename = file_attr[0] + transformation + ' (' + str(copy) + ')' + file_attr[1]
        while filename in current_dir:
            copy += 1
            filename = file_attr[0] + transformation + ' (' + str(copy) + ')' + file_attr[1]
    image.save(filename)


def gaussian_noise(image, amount, alpha):
    noise_filter = Image.effect_noise(image.size, amount).convert(image.mode)
    Image.blend(image, noise_filter, alpha=alpha).show()


def logic_handler(image, args, filename):
    fill = args.fill
    file_attr = os.path.splitext(filename)
    current_dir = os.listdir(os.getcwd())
    if args.flr:
        save_file(flip_left_right(image), file_attr, '_flr', current_dir)
    if args.ftb:
        save_file(flip_top_bottom(image), file_attr, '_ftb', current_dir)
    if args.rot:
        save_file(rotate(image, args.rot, fill), file_attr, '_rot', current_dir)
    if args.ranrot:
        if args.ranrot[0] < args.ranrot[1]:
            save_file(rotate(image, random.randint(args.ranrot[0], args.ranrot[1]), fill), file_attr, '_ranrot', current_dir)
        else:
            print('[-]LOWERBOUND must be smaller than UPPERBOUND')
    if args.trs:
        save_file(translate(image, args.trs[0], args.trs[1], fill), file_attr, '_trs', current_dir)
    if args.gau:
        save_file(gaussian_blur(image, args.gau), file_attr, '_gau', current_dir)
    if args.rangau:
        if (args.rangau[0] > 0 and args.rangau[1] > 0) and (args.rangau[0] < args.rangau[1]):
            save_file(gaussian_blur(image, random.randint(args.rangau[0], args.rangau[1])), file_attr, '_gau', current_dir)
        else:
            print ('[-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')
    if args.sha:
        for i in range(args.sha):
            image = sharpen(image)
        save_file(image, file_attr, '_sha', current_dir)
    if args.ransha:
        if (args.ransha[0] > 0 and args.ransha[1] > 0) and (args.ransha[0] < args.ransha[1]):
            for i in range(random.randint(args.ransha[0], args.ransha[1])):
                image = sharpen(image)
            save_file(image, file_attr, '_ransha', current_dir)
        else:
            print ('[-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')
    if args.crop:
        save_file(crop(image, args.crop[0], args.crop[1], args.crop[2], args.crop[3]), file_attr, '_crop', current_dir)
    if args.rancrop:
        if args.rancrop[0] < image.size[0] and args.rancrop[1] < image.size[1]:
            left = random.randint(0, image.size[0] - args.rancrop[0])
            upper = random.randint(0, image.size[1] - args.rancrop[1])
            save_file(crop(image, left, upper, left + args.rancrop[0], upper + args.rancrop[1]), file_attr, '_rancrop', current_dir)
    if args.gnoi:
        save_file(gaussian_noise(image, args.gnoi[0], args.gnoi[1]), file_attr, '_gnoi', current_dir)
    if args.rangnoi:
        if (args.rangnoi[0] > 0 and args.rangnoi[1] > 0) and (args.rangnoi[0] < args.rangnoi[1]):
            save_file(gaussian_noise(image, random.randint(args.rangnoi[0], args.rangnoi[1]), args.rangnoi[2]), file_attr, '_gnoi', current_dir)
        else:
            print ('[-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')



def main():
    args = parser.parse_args()

    if os.path.isfile(args.input):
        try:
            image = Image.open(args.input)
            logic_handler(image, args, args.input)
        except UnidentifiedImageError:
            print ("[-]Invalid image file provided")
    elif os.path.isdir(args.input):
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
