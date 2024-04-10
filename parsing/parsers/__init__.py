import typing as tp

from parsing.parsers.default_scraper import DefaultScraper
from parsing.parsers.bestchange_scraper import BestChangeScraper  # noqa # pylint: disable=unused-import


def get_place_api_by_site_name(place_name: str) -> tp.Type[DefaultScraper]:
    """
    Determine API class by its name
    """
    for site_api_class in list(DefaultScraper.__subclasses__()):
        if hasattr(site_api_class, 'PLACE_NAME'):
            if site_api_class.PLACE_NAME == place_name:
                return site_api_class
    raise NotImplementedError()
