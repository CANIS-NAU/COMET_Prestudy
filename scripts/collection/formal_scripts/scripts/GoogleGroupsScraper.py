#!/usr/bin/env python3

# imports
from time import sleep
from BaseScraper import DriverType, Scraper, Post
from selenium.webdriver.common.by import By
from dataclasses import dataclass

# global variables (keep minimal)


@dataclass
class GooglePost(Post):
    """Define any extra fields that are necessary for storing relevant Google Posts data"""

    def to_str(self):
        """converts post items into new-line separated values for file output, Will be changed when actual output format is decided"""

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
                for author, reply in self.replies.items()) + '\n\n')


class GoogleGroupsScraper(Scraper):

    ########## Public Methods ##########
    def __init__(self, site_url: str, keywords_file: str, driver: DriverType):
        super().__init__(site_url, keywords_file, driver)

    def _next_page(self) -> bool:
        """For Google Groups, this function handles moving to the
        next page to gather more data from subsequent 'paginated' pages

        Returns
        -------
        bool
            If True, there are still pages that need to be grabbed, continue
            the operation. If False, we have reached the end of the pages, stop
            the operation.
        """

        # identify 'next page' button
        next_page_button = self.driver.find_element(
            By.XPATH,
            "(//div[@role='button' and @aria-label='Next page'])[1]//span[@aria-hidden='true']",
        )

        next_page_button_parent = self.driver.find_element(
            By.XPATH, "(//div[@role='button' and @aria-label='Next page'])[1]"
        )

        # if next page button is available
        sleep(1)
        is_disabled = next_page_button_parent.get_attribute("aria-disabled") != None
        if is_disabled:
            # let the user know that this is the last page of the website
            print("Last page reached...")
            return False
        # else
        else:
            # click the button
            sleep(
                1
            )  # take a sec to load the page. If it goes to fast, the 'next page' button wont load in
            next_page_button.click()
            return True

    def scrape(self):
        """Go and gather each post, save them to the self.posts buffer"""

        for keyword in self.keywords:

            # enter the search term to navigate to the wanted query page
            self.search(keyword)

            # Identify all posts from within the current query
            posts = self._find_posts()

            if posts:
                for post in posts:
                    self.goto(post)
                    self._new_post(keyword)

            else:
                print(f"No results for keyword: {keyword}")

    def search(self, search_term: str):
        """For Google Groups, navigate to the search bar and
        enter the search terms. Then search the group and return
        the resulting page

        Args:
            search_term (str): keyword/query that you wish to enter into the search bar
        """

        # format string to make manual get request
        get_syntax = "search?q="
        get_space_char = "%20"
        query = get_syntax + search_term.replace(" ", get_space_char)

        # go to the page with newly formatted request string for url
        self.goto(self.base_url + "/" + query)

    ########## Private Methods ##########
    def _find_posts(self) -> list[str]:
        """Identify new posts on current page.

        In the case of Google Groups, all posts are all filtered <a> tags
        containing '/c/' located in the root page

        Returns:
            list[str]: list of urls for all identified posts located in the group
        """

        parsed_links = []

        # emulation of a do-while loop
        while True:

            # grabs all of the clickable links to each post (no duplicates) and returns array of links
            if any(self.driver.find_elements(By.XPATH, "//div[@role='main']/h1")):
                return None

            else:
                post_links = self.driver.find_elements(
                    By.XPATH, "//div[@role='gridcell']/a[contains(@href, '/c/')]"
                )
                for links in post_links:
                    parsed_links.append(links.get_attribute("href"))

            if not self._next_page():
                break

        return parsed_links

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
        return {
            "title": title,
            "author": author,
            "content": content,
            "replies": replies
        }

    def _expand_all_posts(self):
        """Helper function just for Google Groups...
        From within the google groups page, make sure that all posts are expanded
        by clicking the 'expand all' button on the page.
        """

        # identify the expand all button on the page
        expand_button = self.driver.find_elements(
            By.XPATH, "//div[@role='button' and @aria-label='Expand all']"
        )
        if any(expand_button):
            expand_button.pop().click()

    def _new_post(self, keyword: str):
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
        )

        if keyword not in self.posts:
            self.posts[keyword] = [newPost]
        else:
            self.posts[keyword].append(newPost)

    def _get_content(self) -> str:
        """Helper function just for Google Groups...

        Identifies which page elements are the **Original Post Body Content**
        and returns the post text.

        Returns
        -------
        str
            Text content from the original post
        """
        # find the part of the post webpage that contains <html-blob> tag
        value = self.driver.find_element(By.XPATH, "(//div[@role='region' ])[1]").text
        return value

    def _get_post_author(self) -> str:
        """Helper function just for Google Groups...

        Identifies which page element(s) contain **Author Name Content** 
        and returns the original post's author's name as a string

        Returns
        -------
        str
            Post author's name
        """
        value = self.driver.find_element(By.XPATH, "(//h3)[1]").text
        return value

    # NOTE: Side-effect, if a single person replies multiple times in the same post, all reply strings
    # are attached to the same single author in the dictionary
    def _get_responses(self) -> dict[str:str]:
        """Helper function just for Google Groups...

        Identifies which page elements contain **Response Content** and 
        returns a dictionary of strings with the following format:

        ``{author:response, author2:response2, author3:response3, ...}``

        Returns
        -------
        dict
            Dictionary with grouped reply author and reply body content
        """
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
