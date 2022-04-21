import json
import os

from PIL import Image

from image_processing.load_image import load_image
from image_processing.transform_image import crop, crop_by_solid_color
from settings import Settings
from write_nicknames import write_nicknames_to_csv


def check_color(image: Image.Image, x: int, y: int, color: int) -> bool:
    width, height = image.size
    if x >= width:
        return False
    if y >= height:
        return False
    return image.getpixel((x, y)) == color


def prepare_for_templates() -> None:
    image_folder = Settings.get_save_processed_path()

    image_names = os.listdir(image_folder)

    # todo: in future - get templates file from settings
    with open("templates.json") as json_file:
        templates = json.load(json_file)

    result = []
    for image_num, image_name in enumerate(image_names):

        image = load_image(f"{image_folder}\\{image_name}")
        # split image by symbol

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

            # print(f'end_letter_x: {end_letter_x}')
            # print(f'current_x: {current_x}\nend_letter_x: {end_letter_x}\nwidth:{width}\nheight:{height}')
            # copy part of image
            if end_letter_x > 19:
                end_letter_x -= 15
            if end_letter_x == (width - 1):
                end_letter_x = width
            letter = crop(
                image, current_x, 0, end_letter_x + int(is_problem_split), height
            )
            letter = crop_by_solid_color(letter, color_black)
            letters.append(letter)
            # letter.show()

            # remove letter and black border
            total_width = image.size[0]
            image = crop(image, end_letter_x + int(is_problem_split), 0, width, height)
            image = crop_by_solid_color(image, color_black)
            width, height = image.size

            if end_letter_x == total_width:
                break
            # image.show()
            # break

        # print(templates)

        text = ""
        for letter in letters:
            # letter.show()
            width, height = letter.size
            filtered_templates = [
                d
                for d in templates
                if (
                    width - 1 <= d["width"] <= width + 1
                    and height - 1 <= d["height"] <= height + 1
                )
            ]
            # filtered_templates = templates

            symbol = "?"

            for template in filtered_templates:
                white_points = template["white_points"]
                if white_points:
                    # if any([letter.getpixel(tuple(white_point)) == color_black for white_point in white_points]):
                    if any(
                        [
                            check_color(
                                letter, white_point[0], white_point[1], color_black
                            )
                            for white_point in white_points
                        ]
                    ):
                        # print(f'symbol {template["symbol"]} by white_points')
                        # print(([letter.getpixel(tuple(white_point)) == color_black for white_point in white_points]))
                        continue  # skip template

                black_points = template["black_points"]
                if black_points:
                    # if any([letter.getpixel(tuple(black_point)) != color_black for black_point in black_points]):
                    if any(
                        [
                            check_color(letter, black_point[0], black_point[1], 255)
                            for black_point in black_points
                        ]
                    ):
                        # print(f'symbol {template["symbol"]} by black_points')
                        # print([letter.getpixel(tuple(black_point)) != color_black for black_point in black_points])
                        continue  # skip template
                symbol = template["symbol"]
                break

            # yes, I'm lazy and stupid
            # so maybe in future add this symbol to template
            if (width, height) == (7, 2):
                symbol = "-"

            # if symbol == '?':
            #     print(f'cannot find symbol\navail templates:{filtered_templates}'
            #           f'\nwidth, height = {width, height}')
            # save_image(letter, save_to_folder, f"FUUUUUUCK_idk.png")

            text += symbol

        # if '?' in text:
        #     print(f'Image: {image_name}\nNum: {image_num}')
        # print(f'Image: {image_name}\nNum: {image_num}')
        # print(text)
        result.append({"num": image_num + 1, "file_name": image_name, "nickname": text})
        # save letters
        # for index, letter in enumerate(letters):
        #     save_image(letter, save_to_folder, f"{(index+1):05}")
        # image.show()

    # todo: get result file name from settings
    write_nicknames_to_csv(result)
