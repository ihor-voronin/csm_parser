from typing import List

from PIL import Image

from .crop_methods import crop_by_solid_color
from .transform_image import crop


def split_image_into_letter(image: Image.Image) -> List[Image.Image]:
    width, height = image.size
    color_black = 0  # black
    letters = []

    current_x = 0
    while current_x < width:
        # find_end_letter_x
        end_letter_x = 0

        # try to get separate symbol
        for col in range(current_x + 1, width):
            is_end_of_letter = all(
                [image.getpixel((col, row)) == color_black for row in range(height)]
            )

            if is_end_of_letter:
                end_letter_x = col
                break

        # ok, another way to get separate symbol
        # some letter contact with another by 1 pixel
        is_problem_split = False
        if end_letter_x == 0 and width > 19:
            for col in range(current_x + 2, width):
                count_of_white_pixels = 0
                for row in range(height):
                    if image.getpixel((col, row)) != color_black:
                        count_of_white_pixels += 1

                if count_of_white_pixels <= 1:
                    end_letter_x = col
                    is_problem_split = True
                    break

        # ok, no way worked and I'm miss something
        if end_letter_x == 0:
            end_letter_x = width

        # copy part of image
        if end_letter_x > 19:
            end_letter_x -= 15
        if end_letter_x == (width - 1):
            end_letter_x = width
        letter = crop(image, current_x, 0, end_letter_x + int(is_problem_split), height)
        letter = crop_by_solid_color(letter, color_black)
        letters.append(letter)

        # remove letter and black border
        total_width = image.size[0]
        image = crop(image, end_letter_x + int(is_problem_split), 0, width, height)
        image = crop_by_solid_color(image, color_black)
        width, height = image.size

        if end_letter_x == total_width:
            break
    return letters
