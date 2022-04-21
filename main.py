import argparse

from delete_folders import clean_folders
from image_processing.recognize_from_templates import recognize_from_templates
from nickname_recognize import prepare_nicknames
from nickname_saver import save_nicknames
from settings import Settings
from window_controll.window_list import list_of_open_windows


def main() -> None:
    if args.load_settings:
        Settings.load_from_string(args.load_settings)

    if args.display_settings:
        Settings.display_settings()

    if args.windows_list:
        list_of_open_windows()

    if args.window:
        save_nicknames(args.window)

    if args.prepare_nicknames:
        prepare_nicknames()

    if args.recognize_templates:
        recognize_from_templates()

    if args.clean:
        clean_folders()


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
        "-ls",
        "--load-settings",
        help="Load settings params from string in json format",
        type=str,
    )
    parser.add_argument(
        "-wl",
        "--windows-list",
        help="List of open windows with their IDs",
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
    parser.add_argument("-w", "--window", type=int, help="id of window to process")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean used folders")

    args = parser.parse_args()
    config = vars(args)
    # print(config)
    main()
