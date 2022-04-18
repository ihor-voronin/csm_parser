from PIL import Image, ImageOps, ImageChops


def crop(image: Image.Image, x: int, y: int, width: int, height: int) -> Image.Image:
    return image.crop((x, y, width, height))


def grayscale(image: Image.Image) -> Image.Image:
    return ImageOps.grayscale(image)


def invert(image: Image.Image) -> Image.Image:
    return ImageOps.invert(image)


def resize(image: Image.Image, height: int) -> Image.Image:
    height_percent = height / float(image.size[1])
    width_size = int((float(image.size[0]) * float(height_percent)))
    return image.resize((width_size, height))


def crop_by_solid_color(image: Image.Image, color) -> Image.Image:
    bg = Image.new(image.mode, image.size, color)
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


def expand(image: Image.Image, color, border_size: int) -> Image.Image:
    return ImageOps.expand(image, border=border_size, fill=color)
