from typing import List

from PIL import Image


def check_color(image: Image.Image, x: int, y: int, color: int) -> bool:
    width, height = image.size
    if x >= width:
        return False
    if y >= height:
        return False
    return image.getpixel((x, y)) == color


def recognize_letter_from_template(letter: Image.Image, templates: List[dict]) -> str:
    width, height = letter.size
    filtered_templates = [
        d
        for d in templates
        if (
            width - 1 <= d["width"] <= width + 1
            and height - 1 <= d["height"] <= height + 1
        )
    ]
    symbol = "?"

    for template in filtered_templates:
        white_points = template["white_points"]
        if white_points:
            if any(
                [
                    check_color(letter, white_point[0], white_point[1], 0)
                    for white_point in white_points
                ]
            ):
                continue  # skip template

        black_points = template["black_points"]
        if black_points:
            if any(
                [
                    check_color(letter, black_point[0], black_point[1], 255)
                    for black_point in black_points
                ]
            ):
                continue  # skip template
        symbol = template["symbol"]
        break

    # yes, I'm lazy and stupid
    # so maybe in future add this symbol to template
    if (width, height) == (7, 2):
        symbol = "-"

    return symbol
