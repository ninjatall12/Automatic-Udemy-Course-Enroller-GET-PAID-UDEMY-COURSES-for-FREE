import argparse
import logging
from argparse import Namespace
from typing import Tuple, Union

from udemy_enroller import Settings
from udemy_enroller.logging import get_logger
from udemy_enroller.runner import redeem_courses

logger = get_logger()


def enable_debug_logging() -> None:
    """
    Enable debug logging for the scripts

    :return: None
    """
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)
    logger.info(f"Enabled debug logging")


def determine_if_scraper_enabled(
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    studybullet_enabled: bool,
    coursevania_enabled: bool,
) -> tuple[bool, bool, bool, bool, bool]:
    """
    Determine what scrapers should be enabled and disabled

    :return: tuple containing boolean of what scrapers should run
    """
    if (
        not freebiesglobal_enabled
        and not tutorialbar_enabled
        and not discudemy_enabled
        and not coursevania_enabled
        and not studybullet_enabled
    ):
        # Set all to True
        (
            freebiesglobal_enabled,
            tutorialbar_enabled,
            studybullet_enabled,
            discudemy_enabled,
            coursevania_enabled,
        ) = (True, True, True, True, True)

    return (
        freebiesglobal_enabled,
        tutorialbar_enabled,
        discudemy_enabled,
        studybullet_enabled,
        coursevania_enabled,
    )


def run(
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    studybullet_enabled: bool,
    max_pages: Union[int, None],
    delete_settings: bool,
):
    """
    Run the udemy enroller script
    :param bool freebiesglobal_enabled:
    :param bool tutorialbar_enabled:
    :param bool discudemy_enabled:
    :param bool coursevania_enabled:
    :param bool studybullet_enabled:
    :param int max_pages: Max pages to scrape from sites (if pagination exists)
    :param bool delete_settings: Determines if we should delete old settings file
    :return:
    """
    settings = Settings(delete_settings)
    redeem_courses(
        settings,
        freebiesglobal_enabled,
        tutorialbar_enabled,
        discudemy_enabled,
        coursevania_enabled,
        studybullet_enabled,
        max_pages
    )


def parse_args() -> Namespace:
    """
    Parse args from the CLI or use the args passed in

    :return: Args to be used in the script
    """
    parser = argparse.ArgumentParser(description="Udemy Enroller")

    parser.add_argument(
        "--freebiesglobal",
        action="store_true",
        default=False,
        help="Run freebiesglobal scraper",
    )

    parser.add_argument(
        "--tutorialbar",
        action="store_true",
        default=False,
        help="Run tutorialbar scraper",
    )

    parser.add_argument(
        "--discudemy",
        action="store_true",
        default=False,
        help="Run discudemy scraper",
    )

    parser.add_argument(
        "--coursevania",
        action="store_true",
        default=False,
        help="Run coursevania scraper",
    )

    parser.add_argument(
        "--studybullet",
        action="store_true",
        default=False,
        help="Run studybullet scraper",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help=f"Max pages to scrape from sites (if pagination exists) (Default is 5)",
    )

    parser.add_argument(
        "--delete-settings",
        action="store_true",
        default=False,
        help="Delete any existing settings file",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
        (
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            studybullet_enabled,
        ) = determine_if_scraper_enabled(
            args.freebiesglobal, args.tutorialbar, args.discudemy, args.coursevania, args.studybullet
        )
        run(
            freebiesglobal_enabled,
            studybullet_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            args.max_pages,
            args.delete_settings,
        )
