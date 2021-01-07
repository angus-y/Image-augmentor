import os,sys
from PIL import Image, ImageFilter, ImageMath
import random
import numpy as ny

im1 = Image.open("C://Users//Admin//Desktop//Python//imeg//tjclogo.jpg")
im2 = Image.open("C://Users//Admin//Desktop//Python//imeg//annoying.jpeg")

# Generating 8 new images of the same image from 8 intervals of rotatin

def rotateInterval(image):
    count = 0
    while count <= 7:
        angle_rotate = count * 45
        image.rotate(angle_rotate).show()
        count+=1


# Flipping the image top-down, left-right, top-down and left-right

def flipImage(image):
    left_right = image.transpose(Image.FLIP_LEFT_RIGHT)
    top_bot = image.transpose(Image.FLIP_TOP_BOTTOM)
    top_bot_left_right = top_bot.transpose(Image.FLIP_LEFT_RIGHT)

    left_right.show()
    top_bot.show()
    top_bot_left_right.show()


# Scaling the image (Zooming in)

def zoomIn(image, interval, no_of_intervals):
    count=1
    while count <= no_of_intervals:
        scale = count*interval
        width = image.width
        height = image.height
        offset_width = float(width) * scale
        offset_height = float(height) * scale
        scaled_im = image.resize(image.size, 3, (offset_width, offset_height, float(width)-offset_width, float(height)-offset_height), None)
        scaled_im.show()
        count+=1


# Cropping the image randomly 10 times

def cropAR(image, scale, no_of_times):
    count = 1
    box_width = int(scale*float(image.width))
    box_height = int(scale*float(image.height))
    while count <= no_of_times:
        left_random = random.randrange(0, image.width-box_width)
        upper_random = random.randrange(0, image.height-box_height)
        im_crop = image.crop((left_random, upper_random, box_width + left_random, box_height + upper_random)).show()
        count += 1



def cropNoAR(image, box_width, box_height, no_of_times):
    count = 1
    while count <= no_of_times:
        left_random = random.randrange(0, image.width-box_width)
        upper_random = random.randrange(0, image.height-box_height)
        im_crop = image.crop((left_random, upper_random, box_width + left_random, box_height + upper_random)).show()
        count += 1

# Translating the image

def translate(image, x, y):
    image.transform(image.size, Image.AFFINE, (1,0,x,0,1,y)).show()

# Blur Image

def normalBlur(image):
    return image.filter(ImageFilter.BLUR())

# Box Blur:

def boxBlur(image, radius):
    return image.filter(ImageFilter.BoxBlur(radius))


# Gaussian Blur

def gaussBlur(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius))


# Gaussian gaussNoise

def gaussNoise(image, power):
    gaussImage = Image.effect_noise(image.size, power).convert('RGB')
    return Image.blend(image, gaussImage, alpha=0.5)


