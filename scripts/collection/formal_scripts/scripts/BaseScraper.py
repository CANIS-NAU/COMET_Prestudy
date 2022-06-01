#!/usr/bin/env python3

# imports
from abc import ABC, abstractmethod
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(self, base_url: str, keywords_file: str | None, driver: str | None, age_threshold: str | None):
        """Constructor to initialize the Scraper object

        NOTE: Web drivers need to be installed prior to use. They will be assumed to be accessible within the system's PATH variable

        The simplified workflow is as follows:
        Create the Scraper object -> Scrape the specified page (storing data in the process) -> Flush/output the structured data to file

        **Example:** ::

            scraper = Scraper("website.com", '/keyword/file/path.txt', '2017', DriverType.CHROME)

            scraper.scrape()

            scraper.flush_posts('/home/user/Downloads/outfile.csv') # Creates the outputted data file at the specified directory

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
        self.driver = self._get_driver(driver)
        self.age_threshold = datetime.strptime(age_threshold, "%m/%Y") if age_threshold is not None else datetime(1,1,1) # set the oldest time threshold to "beginning of time"
        self.posts = []

        if keywords_file is not None:
            self._load_keywords(keywords_file)

    ######## Needs Implementation ########

    @abstractmethod
    def _collect_page_metadata(self) -> dict:
        """Abstraction layer that Gathers the needed page items from the currently loaded post.
        This includes storing the data into a properly structured dictionary that can be
        added to the self.posts dictionary

        You can use/create any amount of helper functions to accomplish this goal,
        as long as, in the end, it returns a dictionary of the required data that can be
        used to add to the self.posts dictionary with the contained data.

        The Dictionary structure is, rougly,  as follows:
            {'post_id': id#, 'username': name, 'date': date, 'content': content, 'replies': {'reply_id: id, 'reply_date': ... } ...}
        """

    @abstractmethod
    def _find_posts(self) -> list[str]:
        """Based on how the website is structured, you will define what a "post" is
        (like a list urls after a search query, or a type of page element, for example) and
        gather all copies of every post that can be identified

        example:
            For Google Groups, a post is defined as "Any <a> tag that contains the value '/c/
            within the href attribute. That logic will be applied here and search for any page elements
            that meet those conditions.

        Returns:
            list[str]: list of urls for all identified posts located in the webpage

        **NOTE:** Will likely need the help of a 'next_page' function to access
        more data if it is hidden behind pagination/loading-screens/etc."""

    def search(self, search_term: str):
        """Enter keyword(s) search into the desired page. the Self.driver class member will act as the
        selenium WebDriver object with the loaded query results page. If no selenium driver is needed for
        this operation, this function can just be used as an abstraction layer for "searching" using an API, for example.

        Parameters
        ----------
        search_term : str
            The keyword that will be searched for. Will be entered into the website's search functionality
            and generate posts that will be eventually scraped.
        """
        pass

    @abstractmethod
    def scrape(self):
        """This user-accessible method is responsible for conducting all scrape operations.
        This method is, essentially the 'main method' of this class. It will
        use all functionality in order to: Navigate to a webpage, Search for
        requested keywords, Scrape resulting search queries for data, and finally
        save that data into a Post data structure within the Scraper object.
        """
        pass

    

    @abstractmethod
    def _new_post(self, keyword: str):
        """With the information gathered from _collect_page_metadata(), append the page data into this object's self.posts variable.
        """
        pass

    ########## END - Needs Implementation ##########

    ########## Class methods that will be shared by all children ##########
    def close(self):
        """**Only needed if Selenium is used for the scraping operation**

        Wrapper around WebDriver.close() when the operation is completed
        """
        self.driver.close()

    def goto(self, url):
        """
        Navigate to the page specified by the `url` parameter, wrapper around
        Selenium's `WebDriver.get()`

        Can be overridden to handle similar functionality without selenium
        Example:
            using *requests* to make a get request to a specific url

        Args:
            url (str): the url of the website you wish to navigate to
        """

        self.driver.get(url)

    def flush_posts(self, filename):
        """Flush all the posts saved in the self.post Dataframe, and output to a file at the
        specified output directory. The output data will be structured using a pandas DataFrame to generate
        a csv file.

        Args:
            filename (str): full directory + filename where the file will be saved and data will be written to
        """

        self.posts.to_csv(filename, sep="\t", index=False)
        print("[INFO] Data outputted to file: {}".format(filename))

    ######## Private Class Functions ########
    def _get_driver(self, driver_name: str):
        """Based on input, return a driver object that
        corresponds to the required web browser

        Args:
            driver_name (DriverType): name of the driver that is desired; (Chrome, Firefox, Opera, Safari)

            The driver can be set to ``None`` which will tell the script not to use Selenium for the scraping process.

        Returns:
            WebDriver: The selenium webdriver object for the requested web browser
        """

        if driver_name == 'chrome':
            options = Options()
            #options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            return webdriver.Chrome(options=options)

        # TODO - settings
        elif driver_name == 'firefox':
            return webdriver.Firefox()

        # TODO - settings
        elif driver_name == 'safari':
            return webdriver.Safari()

        # TODO - settings
        elif driver_name == 'opera':
            return webdriver.Opera()

        elif driver_name == None:
            return None

        else:
            raise Exception("Invalid DriverType Object")

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
