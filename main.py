import argparse

from image_processing.delete_images import delete_images
from image_processing.template_image import prepare_for_templates
from nickname_recognize import prepare_nicknames
from nickname_saver import save_nicknames
from window_controll.window_list import list_of_open_windows


def main() -> None:
    if args.windows_list:
        list_of_open_windows()

    if args.window:
        save_nicknames(args.window)

    if args.prepare_images:
        prepare_nicknames()

    if args.prepare_templates:
        # base_params_of_letters()
        prepare_for_templates()


    if args.clean:
        # todo: clean all images
        delete_images()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="user converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-wl",
        "--windows-list",
        help="Display list with available windows",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--prepare-images",
        help="preprocess images for recognize",
        action="store_true",
    )
    parser.add_argument(
        "-pt",
        "--prepare-templates",
        help="prepare symbols for templates",
        action="store_true",
    )
    parser.add_argument("-w", "--window", type=int, help="id of window to process")
    parser.add_argument(
        "-c", "--clean", action="store_true", help="clean image folder after processing"
    )

    args = parser.parse_args()
    config = vars(args)
    # print(config)
    main()
