import asyncio
import logging
import datetime
from typing import List

from bs4 import BeautifulSoup

from udemy_enroller.http import get
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = logging.getLogger("udemy_enroller")
x=datetime.datetime.now()
month=x.strftime("%M")

class StudyBulletScraper(BaseScraper):
    """
    Contains any logic related to scraping of data from studybullet.com
    """

    DOMAIN = "https://studybullet.com"

    def __init__(self, enabled, max_pages=None):
        super().__init__()
        self.scraper_name = "studybullet"
        if not enabled:
            self.set_state_disabled()
        self.max_pages = max_pages

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Called to gather the udemy links

        :return: List of udemy course links
        """
        links = await self.get_links()
        logger.info(
            f"Page: {self.current_page} of {self.last_page} scraped from studybullet.com"
        )
        self.max_pages_reached()
        return links

    async def get_links(self) -> List:
        """
        Scrape udemy links from Studybullet.com

        :return: List of udemy course urls
        """
        freebiesglobal_links = []
        self.current_page += 1
        coupons_data = await get(
            f"{self.DOMAIN}/{x.year}/{month}/{x.day}/page/{self.current_page}"
        )
        soup = BeautifulSoup(coupons_data.decode("utf-8"),"html.parser")

        for course_card in soup.find_all('a',class_='thumbnail-link'
        ):

          freebiesglobal_links.append(course_card["href"])

        links = await self.gather_udemy_course_links(freebiesglobal_links)

        for counter, course in enumerate(links):
            logger.debug(f"Received Link {counter + 1} : {course}")

        self.last_page = self._get_last_page(soup)

        return links

    @classmethod
    async def get_udemy_course_link(cls, url: str) -> str:
        """
        Gets the udemy course link

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """
        data = await get(url)
        soup = BeautifulSoup(data.decode("utf-8"),"html.parser")
        for link in soup.find_all('a', class_='enroll_btn'):
            udemy_link = cls.validate_coupon_url(link["href"])

            if udemy_link is not None:
                return udemy_link

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Async fetching of the udemy course links from studybullet.com

        :param list courses: A list of studybullet.com course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return [
            link
            for link in await asyncio.gather(*map(self.get_udemy_course_link, courses))
            if link is not None
        ]

    @staticmethod
    def _get_last_page(soup: BeautifulSoup) -> int:
        """
        Extract the last page number to scrape

        :param soup:
        :return: The last page number to scrape
        """

        return max(
            [
                int(i.text)
                for i in soup.find('ul', class_='page-numbers').find_all('li')
                if i.text.isdigit()
            ]
        )
