#!/usr/bin/env python3

# imports
from ...baseClasses.Scraper import Scraper
from ...baseClasses.Post import Post

# global variables (keep minimal)


class GoogleGroupsScraper(Scraper):

    def __init__(self, site_url: str, keywords: list, driver: str):
        super().__init__(site_url, keywords, driver)

    def to_post(self):
        newPost = Post(title=self.get_post_title(), content=self.get_post_text_content(), responses=self.get_post_responses(), media=None )
        self.posts.append(newPost)

    def get_post_title(self):
        return self.driver.title

    def get_post_text_content(self):
        pass

    def get_post_metadata(self):
        pass

    def get_post_responses(self):
        pass

    def next_page(self):
        pass 

    def scrape(self):
        pass 

    def search(self, search_term: str):
        pass



# navigate to the google groups website in question

# identify valid posts
    # extract title information

    # extract post body

    # recursively extract each reply from each post