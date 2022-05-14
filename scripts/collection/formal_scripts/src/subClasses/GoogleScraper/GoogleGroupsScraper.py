#!/usr/bin/env python3

# imports
from ...baseClasses.Scraper import Scraper
from ...subClasses.GoogleScraper.GooglePost import GooglePost
from selenium.webdriver.common.by import By

# global variables (keep minimal)


class GoogleGroupsScraper(Scraper):

    ########## Public Methods ##########
    def __init__(self, site_url: str, keywords: list, driver: str):
        super().__init__(site_url, keywords, driver)

    def next_page(self):
        pass

    def scrape(self):
        """Go and gather each post, save them to the self.posts buffer
        """
        posts = self._find_posts()

        for post in posts:
            self.goto(post)
            self._new_post()

    def search(self, search_term: str):
        pass

    ########## Private Methods ##########
    def _find_posts(self) -> list[str]:
        """Identify new posts on current page.

        In the case of Google Groups, all posts are all filtered <a> tags
        containing '/c/' located in the root page

        Returns:
            list[str]: list of urls for all identified posts located in the group

        #TODO implement pagination support to go to next page
        """
        return set(
            [
                a_tag.get_attribute("href")
                for a_tag in self.driver.find_elements(by=By.TAG_NAME, value="a")
                if "/c/" in a_tag.get_attribute("href")
            ]
        )
    def _collect_page_metadata(self):

        self._expand_all_posts()

        title = self.driver.title
        author = self._get_post_author()
        content = self._get_content()
        replies = self._get_responses()
        media = None
        return {"title": title, "author": author, "content": content, "replies": replies, "media": media}

    def _expand_all_posts(self):
        """From within the google groups page, make sure that all posts are expanded 
        by clicking the 'expand all' button on the page.
        """

        # identify the expand all button on the page
        expand_button = self.driver.find_elements(By.XPATH, "//div[@role='button' and @aria-label='Expand all']")
        if any(expand_button):
            expand_button.pop().click()


    def _new_post(self):
        metadata = self._collect_page_metadata()
        newPost = GooglePost(
            title=metadata["title"],
            author=metadata["author"],
            post_content=metadata["content"],
            replies=metadata["replies"],
            media=metadata["media"])

        self.posts.append(newPost)

    def _get_content(self) -> str:
        # find the part of the post webpage that contains <html-blob> tag
        value = self.driver.find_element(By.XPATH, "(//div[@role='region' ])[1]").text
        return value

    def _get_post_author(self) -> str:
        value = self.driver.find_element(By.XPATH, "(//h3)[1]").text
        return value

    #NOTE: Side-effect, if a single person replies multiple times in the same post, all reply strings 
    # are attached to the same single author in the dictionary
    def _get_responses(self) -> dict[str:str]:
        # find lists of authors and their replies
        author_str = self.driver.find_elements(By.XPATH, "(//h3)[position()>1]")
        response_str = self.driver.find_elements(By.XPATH, "(//div[@role='region' ])[position()>1]")

        # stitch together both lists into dictionary with structure {author:response}
        value = {author_str[iter].text:response_str[iter].text for iter in range(len(response_str))}
        return value


########## Main function that actually uses this script for scraping ##########
def main():
    # navigate to the google groups website in question

    # identify valid posts
    # extract title information

    # extract post body

    # extract each reply from each post
    pass

if __name__ == '__main__':
    main()