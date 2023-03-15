from PIL import Image

chars = [".", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@"]


def image_to_ascii_art(image):
    pixels = image.getdata()

    # replace each pixel with a character from array
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_width = 120
    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image_string = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image_string = "\n".join(ascii_image_string)
    return ascii_image_string


def resize_for_ascii(image_path):
    img = Image.open(image_path)  # create image object
    # resize the image
    width, height = img.size
    aspect_ratio = height / width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    return img.resize((new_width, int(new_height)))


def grayscale(image):
    # convert image to greyscale format
    return image.convert('L')


def convert_Image_To_Ascii(imagePath):
    return image_to_ascii_art(grayscale(resize_for_ascii(imagePath)))
