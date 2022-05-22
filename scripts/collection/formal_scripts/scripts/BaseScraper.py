#!/usr/bin/env python3

# imports
from selenium import webdriver
from abc import abstractmethod, ABC
from enum import Enum, auto
from dataclasses import dataclass
from selenium.webdriver.chrome.options import Options


class DriverType(Enum):
    """Selection variables, used when selecting the Selenium WebDriver type for
    :func:`~Scraper._get_driver()`"""

    CHROME = auto()
    FIREFOX = auto()
    SAFARI = auto()
    OPERA = auto()


@dataclass
class Post(ABC):
    """Post will act as a "data structure" for abstracting data storage for post data.
    This includes Post titles, text content, responses, digital media, and others.
    These fields can be expanded upon to handle more types of data by creating new subclasses.
    """

    title: str
    author: str
    post_content: str
    replies: dict[str, str]
    # Can add other data points in subclasses based on needs of the website

    @abstractmethod
    def to_str(self):
        """TODO - Set a standard TSV organization style for output.

        This method is used for converting the data within the Post object into a string format for saving to file.
        This will automatically format this object's contents to the desired output
        format (ie. JSON, CSV, TSV, etc.)
        """
        pass


# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(self, base_url: str, keywords_file: str, driver: DriverType, driver_path: str | None):
        """Constructor to initialize the Scraper object

        NOTE: Web drivers need to be installed prior to use

        The simplified workflow is as follows:
        Create the Scraper object -> Scrape the specified page (storing data in the process) -> Flush/output the structured data to file for later use

        **Example:** ::

            scraper = Scraper("website.com", '/keyword/file/path.txt', DriverType.CHROME)

            scraper.scrape()

            scraper.flush_posts('/home/user/Downloads/outfile.txt') # Creates the outputted data file at the specified directory

        Parameters
        ----------
        base_url : str
            The "base url" of the website you wish to scrape. This should be the
            root-level of the website, where all posts can be accessed/searched for.

        keywords_file : str
            The file directory for a file of keywords. This keywords file should be
            line-separated, with one 'keyword/search term' per line.

            *example:*

                internet access

                ookla

                speed test

                ...

        driver : DriverType
            The type of driver you wish to use for automating the website access.
            This is essentially the web browser that you wish to use. For whichever
            driver you choose, make sure that you have the corresponding WebDriver
            binary downloaded and accessable via the PATH system variable.
        """

        self.base_url: str = base_url
        self.keywords: list[str] = []
        self.driver = self._get_driver(driver, driver_path)
        self.posts: dict[str : list[Post]] = {}

        self._load_keywords(keywords_file)

    ######## Needs Implementation ########

    @abstractmethod
    def search(self, search_term: str):
        """Enter keyword(s) search into the desired page. the Self.driver class member will act as the
        selenium WebDriver object with the loaded query results page

        Parameters
        ----------
        search_term : list[str]
            A list of keywords. These will be entered into the website's search bar
            and generate posts that will be eventually scraped.
        """
        pass

    def scrape(self):
        """This function is responsible for conducting all scrape operations.
        This method is, essentially the 'main method' of this class. It will
        use all functionality in order to: Navigate to a webpage, Search for
        requested keywords, Scrape resulting search queries for data, and finally
        save that data into a Post data structure within the Scraper object.
        """
        # iterate through all provided keywords
        for keyword in self.keywords:

            # search
            self.search(keyword)

            # collect post urls from search query
            post_urls = self._find_posts()

            # if results exist
            if post_urls:

                # store item into the Scraper.posts dictionary
                for post in post_urls:
                    self.goto(post)
                    self._new_post(keyword)

            # else
            else:
                # tell the user that there were no results for this keyword
                print(f"No results for keyword: {keyword}")

    @abstractmethod
    def _find_posts(self) -> list[str]:
        """Based on how the website is structured, you will define what a "post" is
        (like a list urls after a search query, or a type of page element, for example) and
        gather all copies of every post that can be identified

        example:
            For Google Groups, a post is defined as "Any <a> tag that contains the value '/c/
            within the href attribute. That logic will be applied here and search for anything
            that meets those conditions.

        Returns:
            list[str]: list of urls for all identified posts located in the webpage

        **NOTE:** Will likely need the help of the 'next_page' function to access
        more data if it is hidden behind pagination/loading-screens/etc."""

    @abstractmethod
    def _new_post(self, keyword: str):
        """Convert the currently loaded page to a post object,
        extracting the wanted page data, and storing it in a Post
        object. Then, save the post inside of the Scraper's 'self.post'
        dictionary.

        The Dictionary structure is as follows:
            {"search_term": [Post1, Post2, Post3, ...]}
        """
        pass

    ########## END - Needs Implementation ##########

    ########## Class methods that will be shared by all children ##########
    def close(self):
        """Wrapper around WebDriver.close() when the operation is completed
        """
        self.driver.close()

    def goto(self, url):
        """Navigate to the page specified by the `url` parameter, wrapper around
        Selenium's `WebDriver.get()`

        Args:
            url (str): the url of the website you wish to navigate to with selenium
        """

        self.driver.get(url)

    def to_baseurl(self):
        """Take the browser back to the website root"""

        self.driver.get(self.base_url)

    def flush_posts(self, filename):
        """Flush all the posts saved in the self.post buffer, and output to a file at the
        specified output directory. The output data will be structured based on the implementation
        of `post.to_str()` in the Post object

        Args:
            filename (str): full directory + filename where the file will be saved and data will be written to
        """

        Key = 0
        Value = 1

        with open(filename, "a") as out_file:
            for item in list(self.posts.items()):

                # write out the keyword that was used for the subsequent posts
                out_file.write("*****" + item[Key] + "*****" + "\n")

                # write the post data to the file
                for post in item[Value]:
                    out_file.write("\t" + post.to_str())

                    # remove the current item out of the list to save space
                    item[Value].remove(post)

    ######## Private Class Functions ########
    def _get_driver(self, driver_name: DriverType, driver_path: str):
        """Based on input, return a driver object that
        corresponds to the required web browser

        Args:
            driver_name (DriverType): name of the driver that is desired; (Chrome, Firefox, Opera, Safari)

        Returns:
            WebDriver: The selenium webdriver object for the requested web browser
        """

        if driver_name == DriverType.CHROME:
            options = Options()
            #options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            return webdriver.Chrome(chrome_options=options, executable_path=driver_path if driver_path else '')

        # TODO - settings
        elif driver_name == DriverType.FIREFOX:
            return webdriver.Firefox()

        # TODO - settings
        elif driver_name == DriverType.SAFARI:
            return webdriver.Safari()

        # TODO - settings
        elif driver_name == DriverType.OPERA:
            return webdriver.Opera()

        else:
            raise Exception("Invalid DriverType Object")

    @abstractmethod
    def _collect_page_metadata(self) -> dict:
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

    def _load_keywords(self, keywords_dir: str):
        """Helper function to load the keywords directory file as an array
        then append values to the object's keywords array.

        Args:
            keywords_dir (str): directory where the keywords-list file is (including filename)
        """
        if keywords_dir:
            with open(keywords_dir, "r") as keyword_file:
                file_arr = keyword_file.read().splitlines()

            self.keywords = file_arr
