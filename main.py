import argparse

from image_processing import prepare_images_for_recognize
from mysql import select_balance
from os_interaction import clean_folders
from screenshot_of_nickname import create_screenshots_of_nicknames
from settings import Settings
from templates import recognize_images_from_folder
from window_control import get_window_id_from_opened_windows

__version__ = "V1.0.0"

from write_nicknames import write_nicknames_to_csv


def main() -> None:
    all_methods = False
    if (
        vars(args)["window_id"] is False
        and vars(args)["prepare_nicknames"] is False
        and vars(args)["recognize_templates"] is False
        and vars(args)["screenshot_generation"] is None
        and vars(args)["clean"] is False
    ):
        print("all methods activated step by step")
        all_methods = True

    if args.load_settings:
        Settings.load_from_string(args.load_settings)

    if args.load_file:
        Settings.load_from_file(args.load_file)

    if args.display_settings:
        Settings.display_settings()

    if args.clean or all_methods:
        clean_folders()

    window_id = args.screenshot_generation
    if args.window_id or all_methods:
        window_id = get_window_id_from_opened_windows()

    if args.screenshot_generation or all_methods:
        create_screenshots_of_nicknames(window_id)

    if args.prepare_nicknames or all_methods:
        prepare_images_for_recognize()

    if args.recognize_templates or all_methods:
        nicknames = recognize_images_from_folder(Settings.get_save_processed_path())
        remain_money = select_balance()
        write_nicknames_to_csv(nicknames, remain_money=remain_money)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="user converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-ds",
        "--display-settings",
        help="Display current settings params",
        action="store_true",
    )
    parser.add_argument(
        "-lf",
        "--load-file",
        help="Load settings params from file",
        type=str,
    )
    parser.add_argument(
        "-ls",
        "--load-settings",
        help="Load settings params from string in json format",
        type=str,
    )
    parser.add_argument(
        "-w",
        "--window-id",
        help="ID of CSM window among opened windows",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--prepare-nicknames",
        help="preprocess nicknames for recognize",
        action="store_true",
    )
    parser.add_argument(
        "-rt",
        "--recognize-templates",
        help="Recognize nicknames by templates method",
        action="store_true",
    )
    parser.add_argument(
        "-sg",
        "--screenshot-generation",
        type=int,
        help="Generate screenshot of nicknames from selected window. ID of window required for process",
    )
    parser.add_argument("-c", "--clean", action="store_true", help="Clean used folders")

    args = parser.parse_args()
    # config = vars(args)
    # print(config)
    main()
