#!/usr/bin/env python3

# imports
from ..Base.Scraper import Scraper, Post
from selenium.webdriver.common.by import By
from dataclasses import dataclass

# global variables (keep minimal)

@dataclass
class GooglePost(Post):
    """Define fields that are necessary for storing relevant Google Posts data
    """
    media: list[bytes]

    def to_str(self):
        """TODO converts post items into \n separated values,
        Will be changed when actual output format is decided
        """

        newline = "\n"
        tab = "\t"

        return (
            f"Title: {self.title}\n"
            + "Content: "
            + self.post_content.replace("\n", " ")
            + "\n"
            + "Replies:\n"
            + "\n".join(
                f"{tab}{author}: {reply.replace(newline, ' ')}"
                for author, reply in self.replies.items()
            )
            + f"Media: {len(self.media) if self.media else 0} Media items were found\n\n"
        )


class GoogleGroupsScraper(Scraper):

    ########## Public Methods ##########
    def __init__(self, site_url: str, keywords: list, driver: str):
        super().__init__(site_url, keywords, driver)

    # TODO - Pagination Support
    def next_page(self):
        """For Google Groups, this will need to handle clicking to
        the next page of the group to gather the rest of the post
        data
        """
        pass

    def scrape(self):
        """Go and gather each post, save them to the self.posts buffer"""
        posts = self._find_posts()

        for post in posts:
            self.goto(post)
            self._new_post()

    # TODO
    def search(self, search_term: str):
        """For Google Groups, navigate to the search bar and 
        enter the search terms. Then search the group and return
        the resulting page

        Args:
            search_term (str): _description_
        """
        pass

    ########## Private Methods ##########
    def _find_posts(self) -> list[str]:
        """Identify new posts on current page.

        In the case of Google Groups, all posts are all filtered <a> tags
        containing '/c/' located in the root page

        Returns:
            list[str]: list of urls for all identified posts located in the group

        #TODO implement pagination support to go to next page
        #TODO optimize using XPath
        """
        return set(
            [
                a_tag.get_attribute("href")
                for a_tag in self.driver.find_elements(by=By.TAG_NAME, value="a")
                if "/c/" in a_tag.get_attribute("href")
            ]
        )

    def _collect_page_metadata(self) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated (within this object) and 
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }
        """

        self._expand_all_posts()

        title = self.driver.title
        author = self._get_post_author()
        content = self._get_content()
        replies = self._get_responses()
        media = None
        return {
            "title": title,
            "author": author,
            "content": content,
            "replies": replies,
            "media": media,
        }

    def _expand_all_posts(self):
        """From within the google groups page, make sure that all posts are expanded
        by clicking the 'expand all' button on the page.
        """

        # identify the expand all button on the page
        expand_button = self.driver.find_elements(
            By.XPATH, "//div[@role='button' and @aria-label='Expand all']"
        )
        if any(expand_button):
            expand_button.pop().click()

    def _new_post(self):
        """After collecting all post data, use this function to
        organize and place the data in their appropriate fields 
        within the class.
        """
        metadata = self._collect_page_metadata()
        newPost = GooglePost(
            title=metadata["title"],
            author=metadata["author"],
            post_content=metadata["content"],
            replies=metadata["replies"],
            media=metadata["media"],
        )

        self.posts.append(newPost)

    def _get_content(self) -> str:
        # find the part of the post webpage that contains <html-blob> tag
        value = self.driver.find_element(By.XPATH, "(//div[@role='region' ])[1]").text
        return value

    def _get_post_author(self) -> str:
        value = self.driver.find_element(By.XPATH, "(//h3)[1]").text
        return value

    # NOTE: Side-effect, if a single person replies multiple times in the same post, all reply strings
    # are attached to the same single author in the dictionary
    def _get_responses(self) -> dict[str:str]:
        # find lists of authors and their replies
        author_str = self.driver.find_elements(By.XPATH, "(//h3)[position()>1]")
        response_str = self.driver.find_elements(
            By.XPATH, "(//div[@role='region' ])[position()>1]"
        )

        # stitch together both lists into dictionary with structure {author:response}
        value = {
            author_str[iter].text: response_str[iter].text
            for iter in range(len(response_str))
        }
        return value
