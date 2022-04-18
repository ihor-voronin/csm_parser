from PIL import Image

from config import Config
from image_processing.save_image import save_image
from image_processing.screen_shot import screen_shoot
from image_processing.transform_image import crop
from window_controll.window_control import set_window_position, page_down, click


def split_screenshot_to_nicknames(
    image: Image.Image, count: int, start_y: int, name_index_start: int = 0
) -> None:
    save_folder = Config.config()["ImageProcessing"]["path"]
    for image_num in range(count):
        nickname_image = crop(
            image,
            Config.config()["ImageProcessing"].getint("start_nickname_x"),
            start_y
            + (
                image_num * Config.config()["ImageProcessing"].getint("nickname_height")
            ),
            Config.config()["ImageProcessing"].getint("start_nickname_x")
            + Config.config()["ImageProcessing"].getint("nickname_with"),
            start_y
            + (
                (image_num + 1)
                * Config.config()["ImageProcessing"].getint("nickname_height")
            ),
        )
        save_image(
            image=nickname_image,
            name=f"{name_index_start + (image_num+1):05}",
            save_folder=save_folder,
        )


def process_page(
    page_num: int,
    window_id: int,
    full_pgdn_in_page: int,
    nickname_by_pgdn: int,
    count_nickname_after_pgdn: int,
) -> None:
    # click to center of application
    click(
        Config.config()["WindowConfig"].getint("width") / 2,
        Config.config()["WindowConfig"].getint("height") / 2,
    )
    # page down for setup init position
    page_down()

    count_nicknames_in_page = 200

    for step_by_page in range(full_pgdn_in_page):
        # take screen of window
        screen = screen_shoot(window_id=window_id)
        # split and save images
        split_screenshot_to_nicknames(
            image=screen,
            count=nickname_by_pgdn,
            start_y=Config.config()["ImageProcessing"].getint("start_nickname_y"),
            name_index_start=count_nicknames_in_page * page_num
            + nickname_by_pgdn * step_by_page,
        )
        page_down()

    # last nicknames in page
    # todo: to config this parameters (cont of last images)
    screen = screen_shoot(window_id=window_id)
    split_screenshot_to_nicknames(
        image=screen,
        count=count_nickname_after_pgdn,
        start_y=(
            Config.config()["ImageProcessing"].getint("start_nickname_y")
            + (
                Config.config()["ImageProcessing"].getint("nickname_height")
                * (nickname_by_pgdn - count_nickname_after_pgdn + 1)
            )
        ),
        name_index_start=count_nicknames_in_page * page_num
        + nickname_by_pgdn * full_pgdn_in_page,
    )


def save_nicknames(window_id: int):
    # set base position for correct processing
    set_window_position(window_id)

    # click to set default position of nicknames
    click(165, 211)
    full_pgdn_in_page = Config.config()["WindowConfig"].getint("full_pgdn_in_page")
    nickname_by_pgdn = Config.config()["WindowConfig"].getint("nickname_by_pgdn")
    count_nickname_after_pgdn = Config.config()["WindowConfig"].getint(
        "count_nickname_after_pgdn"
    )
    full_pgdn_in_last_page = Config.config()["WindowConfig"].getint(
        "full_pgdn_in_last_page"
    )

    count_of_pages = Config.config()["WindowConfig"].getint("count_of_pages")
    for page_mun in range(count_of_pages - 1):
        # print(f"process page {page_mun+1}")
        # click to reset pgdn position
        click(750, 75)
        process_page(
            page_num=page_mun,
            window_id=window_id,
            full_pgdn_in_page=full_pgdn_in_page,
            nickname_by_pgdn=nickname_by_pgdn,
            count_nickname_after_pgdn=count_nickname_after_pgdn,
        )

        click(860, 211)  # click to next page

    # print(f"process page {count_of_pages}")
    process_page(
        page_num=count_of_pages - 1,
        window_id=window_id,
        full_pgdn_in_page=full_pgdn_in_last_page,
        nickname_by_pgdn=nickname_by_pgdn,
        count_nickname_after_pgdn=count_nickname_after_pgdn,
    )
