#!/usr/bin/env python3

# imports
from selenium import webdriver
from abc import abstractmethod, ABC
from .Post import Post

# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(self, base_url: str, search_keywords: list, driver: str):
        """Initialize the Scraper Object

        NOTE: Web drivers need to be installed prior to use

        Args:
            base_url (str): The url of the root website you wish to scrape
            search_keywords (list): Specific keywords/search terms that you wish to enter into a search functionality
            driver (str): The driver/browser you wish to use for accessing the internet ("Chrome"/"Firefox/Safari/Opera")
        """

        self.base_url: str = base_url
        self.search_keywords: list[str] = search_keywords
        self.driver = self._get_driver(driver)
        self.posts: list[Post] = []

        self.driver.get(self.base_url)

    ######## Needs Implementation ########

    @abstractmethod
    def search(self, search_term: str):
        """Enter keyword search into the desired page. Self.driver will be the 
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
        """Grabs all post metadata from self.posts array at the provided index. 

        (ie. Post title, post text contents, responses, attached media, etc.)

        Args:
            index (int): index location of the specified post within the 'Posts' array

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
        """meta-function for conducting all scrape operations.
        Acts as an entrypoint for all functionality
        """
        pass

    @abstractmethod
    def _find_posts():
        """Based on how the website is structured, define what a "post" is and
        gather all url's to every post that can be identified
        
        NOTE: Will likely need the help of the 'next_page' function to access 
        more data if it is hidden behind pagination/loading-screens/etc."""

    @abstractmethod
    def _new_post(self):
        """Convert the currently loaded page to a post object, then save within
        the scraper's collection
        """
        pass

    ########## END - Needs Implementation ##########

    ########## Class methods that will be shared by all children ##########
    def goto(self, url):
        """Navigate to the page specified by the `url` parameter

        Args:
            url (str): the url of the website you wish to navigate to with selenium
        """

        self.driver.get(url)

    def to_baseurl(self):
        """Take the browser back to the website root"""

        self.driver.get(self.base_url)

    def flushPosts(self, filename):
        """Flush all the posts saved in the self.post buffer, and output to a file at the
        specified output directory

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
    # TODO Make class constant (ie. Scraper.CHROME) that maps to the proper option, rather than have the user enter a string themselves
    def _get_driver(self, driver_name: str):
        """Based on input, return a driver object that
        corresponds to the required web browser

        Args:
            driver_name (str): name of the driver that is desired; Options: "Chrome, Firefox, Opera, Safari"

        Returns:
            WebDriver: The driver object of the requested web browser
        """
        if "chrome" in driver_name.lower():
            return webdriver.Chrome()

        elif "firefox" in driver_name.lower():
            return webdriver.Firefox()

        elif "safari" in driver_name.lower():
            return webdriver.Safari()

        elif "opera" in driver_name.lower():
            return webdriver.Opera()

        else:
            print("Invalid Driver Name")
            exit(1)

    def _out_file_format():
        """--TODO-- Handles the output of multiple post.to_str() calls, and organizes
        into a single output ready to be written into a file.
        """

    @abstractmethod
    def _collect_page_metadata() -> dict:
        """Gathers the needed page items from the current site loaded by
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