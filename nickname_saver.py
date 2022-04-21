import os

from PIL import Image

from image_processing.save_image import save_image
from image_processing.screen_shot import screen_shoot
from image_processing.transform_image import crop
from progress_bar import progress_bar
from settings import Settings
from window_controll.window_control import (
    click,
    maximize_window,
    minimize_window,
    page_down,
    set_window_position,
)


def split_screenshot_to_nicknames(
    image: Image.Image, count: int, start_y: int, name_index_start: int = 0
) -> None:
    save_folder = Settings.get_save_screenshot_path()
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    for image_num in range(count):
        nickname_image = crop(
            image,
            Settings.page_start_coordinate_nickname_x,
            start_y + (image_num * Settings.page_nickname_height),
            Settings.page_start_coordinate_nickname_x + Settings.page_nickname_width,
            start_y + ((image_num + 1) * Settings.page_nickname_height),
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
        int(Settings.window_width / 2),
        int(Settings.window_height / 2),
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
            start_y=Settings.page_start_coordinate_nickname_y,
            name_index_start=count_nicknames_in_page * page_num
            + nickname_by_pgdn * step_by_page,
        )
        page_down()

    # last nicknames in page
    screen = screen_shoot(window_id=window_id)
    split_screenshot_to_nicknames(
        image=screen,
        count=count_nickname_after_pgdn,
        start_y=(
            Settings.start_coordinate_y
            + (
                Settings.page_nickname_height
                * (nickname_by_pgdn - count_nickname_after_pgdn + 1)
            )
        ),
        name_index_start=count_nicknames_in_page * page_num
        + nickname_by_pgdn * full_pgdn_in_page,
    )


def save_nicknames(window_id: int) -> None:
    print(
        """
Start getting nicknames from the app.
IMPORTANT!!!
Do not move the mouse cursor or click until the window is minimized
    """
    )
    try:
        input("Press Enter to continue...")
    except SyntaxError:
        pass
    # set base position for correct processing
    maximize_window(window_id)
    set_window_position(window_id)

    # click to set default position of nicknames
    click(165, 211)
    full_pgdn_in_page = Settings.PgDn_count_in_full_page
    nickname_by_pgdn = Settings.PgDn_contain_nickname
    count_nickname_after_pgdn = Settings.PgDn_remain_count_nickname
    full_pgdn_in_last_page = Settings.PgDn_count_in_last_page

    count_of_pages = Settings.page_count
    progress_bar(0, count_of_pages, prefix="Progress:", suffix="Complete", length=50)
    for page_mun in range(count_of_pages - 1):
        # click to reset pgdn position
        click(750, 75)
        process_page(
            page_num=page_mun,
            window_id=window_id,
            full_pgdn_in_page=full_pgdn_in_page,
            nickname_by_pgdn=nickname_by_pgdn,
            count_nickname_after_pgdn=count_nickname_after_pgdn,
        )
        progress_bar(
            page_mun + 1,
            count_of_pages,
            prefix="Progress:",
            suffix="Complete",
            length=50,
        )
        click(860, 211)  # click to next page

    process_page(
        page_num=count_of_pages - 1,
        window_id=window_id,
        full_pgdn_in_page=full_pgdn_in_last_page,
        nickname_by_pgdn=nickname_by_pgdn,
        count_nickname_after_pgdn=count_nickname_after_pgdn,
    )
    progress_bar(
        count_of_pages, count_of_pages, prefix="Progress:", suffix="Complete", length=50
    )

    minimize_window(window_id)
    print(f"Nicknames saved to {Settings.get_save_screenshot_path()}")
