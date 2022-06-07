#!/usr/bin/env python3

from datetime import datetime

import pandas as pd
from searchtweets import ResultStream, gen_request_parameters, load_credentials

from BaseScraper import Scraper

class TwitterScraper(Scraper):

    def __init__(self, base_url: str, keywords_file: str | None, age_threshold: str | None) -> None:
        super().__init__(base_url, keywords_file, age_threshold)


    def _collect_page_metadata(self) -> dict:
        raise NotImplementedError

    def _find_posts(self) -> list[str]:
        raise NotImplementedError

    def search(self):
        raise NotImplementedError


def main():
    pass


if __name__ == "__main__":
    main()

