#Author: Angus
import os
import sys
import time
import random
import argparse
from datetime import datetime
from PIL import Image, UnidentifiedImageError, ImageFilter


files_written = 0
parser = argparse.ArgumentParser(description='Image processing script.')
parser.add_argument('-i', '--input', help='Input file/directory path to peform image augmentation on', required=True)
parser.add_argument('-o', '--output', help='Output directory to write augmented images to', default='', type=str)
parser.add_argument('-r', '--repeat', help='Number of times to repeat image augmentations', default=1, type=int)
parser.add_argument('-f', '--force', help='Force the resizing of images such that augmented images have the same dimensions as the original image (can be used for cropping and zooming)', action="store_true") # NOT DONE
parser.add_argument("--flr", help='Perform a left right flip on the image', action="store_true")
parser.add_argument("--ftb", help='Perform a top bottom flip on the image', action="store_true")
parser.add_argument("--trs", metavar=('X','Y'), help='Perform a translation on the image displacing it along the axis by a certain number of X and Y pixels (+ve values translate left and upwards -ve values translate right and downwards)', nargs=2, type=int)
parser.add_argument("--rantrs", metavar=('LOWERBOUND_X','UPPERBOUND_X', 'LOWERBOUND_Y','UPPERBOUND_Y'), help='Perform a random translation on the image between LOWERBOUND and UPPERBOUND displacing it along the x and y axis (+ve values translate left and upwards -ve values translate right and downwards)', nargs=4, type=int)
parser.add_argument("--crop", metavar=('X1','Y1','X2','Y2'), help='Perform an image crop on the bounding box : Upperleft (X1, Y1) and lower right (X2, Y2)', nargs=4, type=int)
parser.add_argument("--rancrop", metavar=('WIDTH', 'HEIGHT'), help='Perform a random image crop to create an image of specific WIDTH and HEIGHT', nargs=2, type=int)
parser.add_argument("--gau", metavar='RADIUS', help='Perform a gaussian blur transformation on the image with a specific pixel RADIUS', type=int)
parser.add_argument("--rangau", metavar=("LOWERBOUND","UPPERBOUND"), help='Perform a gaussian blur transformation on the image with a specific pixel radius randomly chosen between LOWERBOUND and UPPERBOUND', nargs=2, type=int)
parser.add_argument("--box", metavar='RADIUS', help='Perform a box blur transformation on the image with a specific pixel RADIUS', type=int)
parser.add_argument("--ranbox", metavar=("LOWERBOUND","UPPERBOUND"), help='Perform a box blur transformation on the image with a specific pixel radius randomly chosen between LOWERBOUND and UPPERBOUND', nargs=2, type=int)
parser.add_argument("--sha", metavar='ITERATIONS', help='Perform a sharpen transformation on the image for a number of ITERATIONS', type=int)
parser.add_argument("--ransha", metavar=("LOWERBOUND","UPPERBOUND"), help='Perform a sharpen transformation on the image for a number of iterations randomly chosen between LOWERBOUND and UPPERBOUND', nargs=2, type=int)
parser.add_argument("--rot", metavar="DEGREES", help='Perform an image rotation by the specified DEGREES counter clockwise (-ve for clockwise rotation)', type=int)
parser.add_argument("--ranrot", help='Perform a counterclockwise image rotation by a certain number of degrees randomly chosen between LOWERBOUND and UPPERBOUND (-ve for clockwise rotation)',
                    metavar=("LOWERBOUND","UPPERBOUND"), nargs=2, type=int)
parser.add_argument("--gnoi", metavar=("AMOUNT", "ALPHA"), help='Add a certain AMOUNT of gaussian noise to the image blended with a certain ALPHA (between 0 and 1)', nargs=2, type=float)
parser.add_argument("--rangnoi", metavar=("LOWERBOUND", "UPPERBOUND", "ALPHA"), help='Add a certain amount of gaussian noise to the image randomly chosen between LOWERBOUND and UPPERBOUND of a certain ALPHA', nargs=3, type=float)
parser.add_argument("--zoom", metavar=("FACTOR_X", "FACTOR_Y"), help='Center zoom into the image by a certain amount where dimensions of image crop -> (new_size_x, new_size_y) = (old_size_x * FACTOR_X, old_size_Y * FACTOR_Y) original image size is maintained', nargs=2, type=float) #NOT DONE
parser.add_argument("--ranzoom", metavar=("LOWERBOUND_X", "UPPERBOUND_X", "LOWERBOUND_Y", "UPPERBOUND_Y"), help='Center zoom into the image by a random amount between LOWERBOUND and UPPERBOUND where dimensions of image crop -> (new_size_x, new_size_y) = (old_size_x * FACTOR_X, old_size_Y * FACTOR_Y) original image size is maintained', nargs=4, type=float) #NOT DONE
parser.add_argument("--fill", metavar='HEX', help='Replace any newly introduced alpha pixels with pixels of a certain HEX value during any geometric image transformation', type=str)


def flip_left_right(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def flip_top_bottom(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def rotate(image, theta, fill):
    return image.rotate(theta, fillcolor=fill)


def gaussian_blur(image, amount):
    return image.filter(ImageFilter.GaussianBlur(radius=amount))


def box_blur(image, amount):
    return image.filter(ImageFilter.BoxBlur(radius=amount))


def sharpen(image):
    return image.filter(ImageFilter.SHARPEN)


def translate(image, x, y, fill):
    return image.transform(image.size, Image.AFFINE, (1, 0, x, 0, 1, y), fillcolor=fill)


def crop(image, x1, y1, x2, y2):
    return image.crop((x1, y1, x2, y2))


def zoom(image, w_scale, h_scale):
    original_size = image.size
    new_width = round((original_size[0] - original_size[0] / w_scale)/2)
    new_height = round((original_size[1] - original_size[1] / h_scale)/2)
    image = image.crop((new_width, new_height, new_width + original_size[0] / w_scale, new_height + original_size[1] / h_scale))
    return image.resize(original_size)


def save_file(image, file_attr, transformation, current_dir, out_dir):
    global files_written
    filename = file_attr[0] + transformation + file_attr[1]
    if filename in current_dir:
        copy = 1
        while filename in current_dir:
            filename = file_attr[0] + transformation + ' (' + str(copy) + ')' + file_attr[1]
            copy += 1
    image.save(os.path.join(out_dir,filename))
    files_written += 1


def gaussian_noise(image, amount, alpha):
    noise_filter = Image.effect_noise(image.size, amount).convert(image.mode)
    Image.blend(image, noise_filter, alpha=alpha).show()


def premature_exit(message):
    print (message + " - Program prematurely terminated")
    os._exit(1)


def logic_handler(image, args, filename, arg_order):
    ops = []
    fill = args.fill
    file_attr = os.path.splitext(filename)
    if args.output:
        current_dir = os.listdir(args.output)
    else:
        current_dir = os.listdir(os.getcwd())
    for i in arg_order:
        if i == '--flr':
            image = flip_left_right(image)
        elif i == '--ftb':
            image = flip_top_bottom(image)
        elif i == '--rot':
            image = rotate(image, args.rot, fill)
        elif i == '--ranrot':
            if args.ranrot[0] < args.ranrot[1]:
                image = rotate(image, random.randint(args.ranrot[0], args.ranrot[1]), fill)
            else:
                premature_exit('[ranrot-] : LOWERBOUND must be smaller than UPPERBOUND')
        elif i == '--trs':
            image = translate(image, args.trs[0], args.trs[1], fill)
        elif i == '--rantrs':
            if args.rantrs[0] <= args.rantrs[1] and args.rantrs[2] <= args.rantrs[3]:
                image = translate(image, random.randint(args.rantrs[0], args.rantrs[1]), random.randint(args.rantrs[2], args.rantrs[3]), fill)
            else:
                premature_exit('[rantrs-] : LOWERBOUND must be smaller than or equal to UPPERBOUND')
        elif i == '--gau':
            image = gaussian_blur(image, args.gau)
        elif i == '--rangau':
            if (args.rangau[0] > 0 and args.rangau[1] > 0) and (args.rangau[0] < args.rangau[1]):
                gaussian_blur(image, random.randint(args.rangau[0], args.rangau[1]))
            else:
                premature_exit('[rangau-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')
        elif i == '--box':
            image = box_blur(image, args.box)
        elif i == '--ranbox':
            if (args.ranbox[0] > 0 and args.ranbox[1] > 0) and (args.ranbox[0] < args.ranbox[1]):
                image = box_blur(image, random.randint(args.ranbox[0], args.ranbox[1]))
            else:
                premature_exit('[ranbox-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')
        elif i == '--sha':
            for j in range(args.sha):
                image = sharpen(image)
        elif i == '--ransha':
            if (args.ransha[0] > 0 and args.ransha[1] > 0) and (args.ransha[0] < args.ransha[1]):
                for j in range(random.randint(args.ransha[0], args.ransha[1])):
                    image = sharpen(image)
            else:
                premature_exit('[ransha-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')
        elif i == '--crop':
            if args.force:
                image = crop(image, args.crop[0], args.crop[1], args.crop[2], args.crop[3]).resize(image.size)
            else:
                image = crop(image, args.crop[0], args.crop[1], args.crop[2], args.crop[3])
        elif i == '--rancrop':
            if args.rancrop[0] < image.size[0] and args.rancrop[1] < image.size[1]:
                left = random.randint(0, image.size[0] - args.rancrop[0])
                upper = random.randint(0, image.size[1] - args.rancrop[1])
                if args.force:
                    image = crop(image, left, upper, left + args.rancrop[0], upper + args.rancrop[1]).resize(image.size)
                else:
                    image = crop(image, left, upper, left + args.rancrop[0], upper + args.rancrop[1])
            else:
                premature_exit('[rancrop-]Crop WIDTH and HEIGHT size must be smaller than image width and height size')
        elif i == '--gnoi':
            image = gaussian_noise(image, args.gnoi[0], args.gnoi[1])
        elif i == '--rangnoi':
            if (args.rangnoi[0] > 0 and args.rangnoi[1] > 0) and (args.rangnoi[0] < args.rangnoi[1]):
                image = gaussian_noise(image, random.randint(args.rangnoi[0], args.rangnoi[1]), args.rangnoi[2])
            else:
                premature_exit('[rangnoi-]LOWERBOUND and UPPERBOUND must both be greater than 0, LOWERBOUND must be smaller than UPPERBOUND')
        elif i == '--zoom':
            if args.zoom[0] >= 1 and args.zoom[1] >= 1:
                image = zoom(image, args.zoom[0], args.zoom[1])
            else:
                premature_exit('[ranzoom-]Zoom FACTOR_X and FACTOR_Y must be bigger than or equal to 1')
        elif i == '--ranzoom':
            if all(i >= 1 for i in args.ranzoom) and (args.ranzoom[0] <= args.ranzoom[1] and args.ranzoom[2] <= args.ranzoom[3]):
                image = zoom(image, random.randint(args.ranzoom[0], args.ranzoom[1]), random.randint(args.ranzoom[2], args.ranzoom[3]))
            else:
                premature_exit('[ranzoom-]Zoom FACTOR_X and FACTOR_Y must be bigger than or equal to 1, LOWERBOUND must be smaller than or equal to UPPERBOUND')
        ops.append(i.replace('--','_',1))
    save_file(image, file_attr, ''.join(ops), current_dir, args.output)


def init_output_dir(output):
    if os.path.isdir(output):
        print (f'[*]Output directory : "{output}" already exists, all augmented files will be written to there')
    else:
        try:
            os.mkdir(output)
            print (f'[+]Successfully created new output directory : {output}')
        except Exception as e:
            print (f'[-]Error : {str(e)}\n[-]Could not initialize new output directory : {output}')
            os._exit(1)


def main():
    args = parser.parse_args()
    arg_order = [i for i in sys.argv if i.startswith('--')]

    if args.output:
        if not os.path.isabs(args.output):
            args.output = os.path.join(os.getcwd(), args.output)
        init_output_dir(args.output)
    else:
        print (f'[*]Output directory assumed to be same as input directory')


    if os.path.isfile(args.input):
        try:
            for i in range(args.repeat):
                image = Image.open(args.input)
                logic_handler(image, args, args.input, arg_order)
        except UnidentifiedImageError:
            print ("[-]Invalid image file provided")
    elif os.path.isdir(args.input):
        os.chdir(args.input)
        processing_dir_size = len(os.listdir(os.getcwd()))
        files_processed = 0
        for filename in os.listdir(os.getcwd()):
            # print (filename)
            print ("", end=f"\r[*]Files processed: {files_processed+1} out of {processing_dir_size}")
            try:
                for i in range(args.repeat):
                    image = Image.open(filename)
                    logic_handler(image, args, filename, arg_order)
            except UnidentifiedImageError:
                print (f"\n[-]Invalid image file '{filename}' in provided directory")
                return
            except Exception as e:
                print (f"\n[-]Hit error when processing '{filename}'\n[-]Error : {str(e)}")
                break
            files_processed += 1
        print()
    else:
        print (f"[-]'{args.input}' is neither a valid filepath or directory path")


if __name__ == '__main__':
    past = time.time()
    output_dir = main()
    present = time.time()
    print (f'[*]Wrote {files_written} file(s) in {present-past} seconds')
