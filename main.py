import argparse

from delete_folders import clean_folders
from image_processing.recognize_from_templates import recognize_from_templates
from nickname_recognize import prepare_nicknames
from screenshot_of_nickname import create_screenshots_of_nicknames
from settings import Settings
from window_controll.window_list import get_window_id_from_opened_windows


def main() -> None:
    all_methods = False
    print(vars(args))
    if (
        vars(args)["window_id"] is False
            and vars(args)["prepare_nicknames"] is False
            and vars(args)["recognize_templates"] is False
            and vars(args)["screenshot_generation"] is None
            and vars(args)["clean"] is False):
        print("all methods activated step by step")
        all_methods = True

    if args.load_settings:
        print("Settings.load_from_string(args.load_settings)")

    if args.load_file:
        print("Settings.load_from_file(args.load_file)")

    if args.display_settings:
        print("Settings.display_settings()")

    window_id = args.screenshot_generation
    if args.window_id or all_methods:
        window_id = get_window_id_from_opened_windows()

    if args.screenshot_generation or all_methods:
        print(f"create_screenshots_of_nicknames({window_id})")

    if args.prepare_nicknames or all_methods:
        print("prepare_nicknames()")

    if args.recognize_templates or all_methods:
        print("recognize_from_templates()")

    if args.clean or all_methods:
        print("clean_folders()")


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
