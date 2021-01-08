from PIL import ImageDraw, Image, ImageFilter, ImageEnhance
import random

def rotate(image, angle):
    rotated_img = image.rotate(angle)
    rotated_img.show()

def random_rotate(image, angle=None):
    angle = random.randint(-360, 360)
    ranrotate_image = image.rotate(angle)
    ranrotate_image.show()

def flip(image, direction):
    if direction == 'Left Right':
        flip_lr = image.transpose(Image.FLIP_LEFT_RIGHT)
        flip_lr.show()
    if direction == 'Top Bottom':
        flip_tb = image.transpose(Image.FLIP_TOP_BOTTOM)
        flip_tb.show()

def random_flip(image, direction=None):
    direction_types = ['Left Right', 'Top Bottom']
    random_number = random.randint(1, len(direction_types)) - 1
    direction = direction_types[random_number]
    if direction == 'Left Right':
        flip_lr = image.transpose(Image.FLIP_LEFT_RIGHT)
        flip_lr.show()
    if direction == 'Top Bottom':
        flip_tb = image.transpose(Image.FLIP_TOP_BOTTOM)
        flip_tb.show()

def crop(image, box):
    cropped_image = image.crop(box)
    cropped_image.show()

def blur(image, type):
    if type == 'Blur':
        blurred_image = image.filter(ImageFilter.BLUR)
        blurred_image.show()
    if type == 'Gaussian Blur':
        blurred_image = image.filter(ImageFilter.GaussianBlur())
        blurred_image.show()
    if type == 'Box Blur':
        blurred_image = image.filter(ImageFilter.BoxBlur())
        blurred_image.show()

def enhance(image, type, amount):

    if type == 'Brightness':
        enhanced_img = ImageEnhance.Brightness(image)
        enhanced_img.enhance(amount).show()
    if type == 'Colour':
        enhanced_img = ImageEnhance.Color(image)
        enhanced_img.enhance(amount).show()
    if type == 'Contrast':
        enhanced_img = ImageEnhance.Contrast(image)
        enhanced_img.enhance(amount).show()
    if type == 'Sharpness':
        enhanced_img = ImageEnhance.Sharpness(image)
        enhanced_img.enhance(amount).show()

def random_enhance(image, max_amount, type=None):
    amount = random.randint(1, max_amount)
    type = ['Brightness', 'Colour', 'Contrast', 'Sharpness']
    type_number = random.randint(1, len(type)) - 1
    type = type[type_number]

    if type == 'Brightness':
        enhanced_img = ImageEnhance.Brightness(image)
        enhanced_img.enhance(amount).show()
    if type == 'Colour':
        enhanced_img = ImageEnhance.Color(image)
        enhanced_img.enhance(amount).show()
    if type == 'Contrast':
        enhanced_img = ImageEnhance.Contrast(image)
        enhanced_img.enhance(amount).show()
    if type == 'Sharpness':
        enhanced_img = ImageEnhance.Sharpness(image)
        enhanced_img.enhance(amount).show()

def colourbands_inversion(image):
    r, g, b = image.split()
    image = Image.merge('RGB', (b, g, r))
    image.show()

def mask(image, mask_shape, xy):
    if mask_shape == 'Rectangle':
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(xy, 255)
        masked_image = Image.composite(image, mask, mask)
        masked_image.show()
    
    if mask_shape == 'Ellipse':
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(xy, 255)
        masked_image = Image.composite(image, mask, mask)
        masked_image.show()




    
