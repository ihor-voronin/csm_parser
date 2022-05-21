from PIL import Image, ImageChops

from image_processing.transform_image import crop


def crop_by_solid_color(image: Image.Image, color: int) -> Image.Image:
    bg = Image.new(image.mode, image.size, color)
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


def crop_black_border(image: Image.Image) -> Image.Image:
    thresh = 200
    image = image.convert("L").point(lambda x: 255 if x > thresh else 0, mode="1")
    color = image.getpixel((0, 0))
    image = crop_by_solid_color(image=image, color=color)
    return image


def crop_by_color_level(image: Image.Image, color_level: int) -> Image.Image:
    width, height = image.size
    crop_to = width - 1
    for x in range(width - 1, 0, -1):
        is_letter = any(
            [image.getpixel((x, y))[0] < color_level for y in range(height)]
        )
        if is_letter:
            crop_to = x
            break
    return crop(
        image,
        0,
        0,
        crop_to + (15 if width - crop_to > 15 else int(width - crop_to / 2)),
        height,
    )
