#!/usr/bin/env python3

# imports
from selenium import webdriver
from abc import abstractmethod, ABC
from enum import Enum, auto
from dataclasses import dataclass


class DriverType(Enum):
    """Selenium WebDriver type selection enum (for _get_driver)"""

    CHROME = auto()
    FIREFOX = auto()
    SAFARI = auto()
    OPERA = auto()


@dataclass
class Post(ABC):
    """Post will act as a "data structure" for abstracting data storage for post data.
    This includes Post titles, text content, responses, digital media, and others.
    Can be expanded upon by creating new subclasses that add more specific data storage items if needed.
    """

    title: str
    author: str
    post_content: str
    replies: dict[str, str]
    # Can add other data points in subclasses based on needs of the website

    @abstractmethod
    def to_str(self):
        """Method for converting the data item into a parse-able string format for saving to file
        eventually. This will automatically format this object's contents to the desired output
        format (ie. JSON, CSV, etc.)
        """
        pass


# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(self, base_url: str, search_keywords: list, driver: DriverType):
        """Initialize the Scraper Object

        NOTE: Web drivers need to be installed prior to use

        Args:
            base_url (str): The url of the root website you wish to scrape
            search_keywords (list): Specific keywords/search terms that you wish to enter into a search functionality
            driver (str): The driver/browser you wish to use for accessing the internet

        The general workflow is a follows:
            Create the Scraper object -> Scrape the specified page (storing data in the process) -> Flush/output the structured data to file for later use

        example:
        ```
        scraper = Scraper("website.com", ['potatoes', 'corn-chip'], DriverType.CHROME)
        scraper.scrape()
        scraper.flush_posts('/home/user/Downloads/outfile.txt') # Creates the outputted data file at the specified directory
        ```
        """

        self.base_url: str = base_url
        self.search_keywords: str | list[str] = search_keywords
        self.driver = self._get_driver(driver)
        self.posts: list[Post] = []

        self.driver.get(self.base_url)

    ######## Needs Implementation ########

    @abstractmethod
    def search(self, search_term: str | list[str]):
        """Enter keyword(s) search into the desired page. Self.driver will be the
        selenium WebDriver object with the loaded query results page

        Args:
            search_term (str): search term/keyword that will sent to the website
            for query

        Returns:
            WebDriver: selenium WebDriver object with the post-query search
            results page
        """
        pass

    def get_post(self, index: int) -> Post:
        """Simple getter, grabs all post metadata from self.posts array at the provided index.

        (ie. Post title, post text contents, responses, attached media, etc.)

        Args:
            index (int): index location of the specified post within the 'self.posts' array

        Returns:
            Post: Post data object with post elements stored as class members
        """

        return self.posts[index]

    @abstractmethod
    def next_page(self):
        """Technique for moving to the next page of a pagenated website,
        or loading all data points from a dynamically growing page structure.
        """
        pass

    @abstractmethod
    def scrape(self):
        """function for conducting all scrape operations.
        Acts as an entrypoint for all functionality
        """
        pass

    @abstractmethod
    def _find_posts():
        """Based on how the website is structured, define what a "post" is 
        (like a specific url, or a type of page element, for example) and
        gather all copies of every post that can be identified

        NOTE: Will likely need the help of the 'next_page' function to access
        more data if it is hidden behind pagination/loading-screens/etc."""

    @abstractmethod
    def _new_post(self):
        """Convert the currently loaded page to a post object, 
        extracting the wanted page data, and storing it in a Post
        object. Then, save the post inside of the Scraper's 'self.post'
        array
        """
        pass

    ########## END - Needs Implementation ##########

    ########## Class methods that will be shared by all children ##########
    def goto(self, url):
        """Navigate to the page specified by the `url` parameter, wrapper around
        Selenium's `webdriver.get()`

        Args:
            url (str): the url of the website you wish to navigate to with selenium
        """

        self.driver.get(url)

    def to_baseurl(self):
        """Take the browser back to the website root"""

        self.driver.get(self.base_url)

    def flushPosts(self, filename):
        """Flush all the posts saved in the self.post buffer, and output to a file at the
        specified output directory. The output data will be structured based on the implementation
        of `post.to_str()` in the Post object

        Args:
            filename (str): full directory + filename where the file will be saved
        """

        with open(filename, "a") as out_file:
            for post in self.posts:

                # write the post data to the file
                out_file.write(post.to_str())

                # pop the current item out of the list
                self.posts.remove(post)

    ######## Private Class Functions ########
    def _get_driver(self, driver_name: DriverType):
        """Based on input, return a driver object that
        corresponds to the required web browser

        Args:
            driver_name (DriverType): name of the driver that is desired; Options: "Chrome, Firefox, Opera, Safari"

        Returns:
            WebDriver: The selenium webdriver object for the requested web browser
        """
        if driver_name == DriverType.CHROME:
            return webdriver.Chrome()

        elif driver_name == DriverType.FIREFOX:
            return webdriver.Firefox()

        elif driver_name == DriverType.SAFARI:
            return webdriver.Safari()

        elif driver_name == DriverType.OPERA:
            return webdriver.Opera()

        else:
            raise Exception("Invalid DriverType Object")

    @abstractmethod
    def _collect_page_metadata() -> dict:
        """TODO - Discuss if this technique can be optimized.
        
        Gathers the needed page items from the current site loaded by
        WebDriver. Gathers data points that will be used to populate Post
        items with corresponding page data

        You can use/create any amount of helper functions to accomplish this goal,
        as long as, in the end, it returns a dictionary of the required data that can be
        used to create a Post object with the contained data.

        Return example:
        {post_field_name: value, ...}

        or...

        {title: "My internet is really bad, help", content: "Does anyone know what to do about slow internet", replies: ["No, not really?", "same here"]}


        (ie. If the website's title is the same value as the post's title, you would
        use 'driver.title to populate the respective Post.title)
        """
