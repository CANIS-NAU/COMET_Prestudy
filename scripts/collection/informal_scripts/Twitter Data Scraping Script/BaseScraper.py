#!/usr/bin/env python3

# imports
from abc import ABC, abstractmethod
from datetime import datetime


# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(
        self,
        keywords_file: str | None,
        age_threshold: str | None,
    ):
        """Constructor to initialize the Scraper object

        NOTE: Web drivers need to be installed prior to use. They will be assumed to be accessible within the system's PATH variable

        The simplified workflow is as follows:
        Create the Scraper object ==> Scrape the specified page (storing data in the process) ==> Flush/output the structured data to file

        **Example:** ::

            scraper = Scraper("website.com", '/keyword/file/path.txt', '2017', DriverType.CHROME)

            scraper.scrape()

            scraper.flush_posts('/home/user/Downloads/outfile.csv') Creates the outputted data file at the specified directory

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

        """

        self.keywords: list[str] = []
        self.age_threshold = (
            datetime.strptime(age_threshold, "%m/%Y")
            if age_threshold is not None
            else datetime(1, 1, 1)
        )  # set the oldest time threshold to "beginning of time"
        self.posts = []

        if keywords_file is not None:
            self._load_keywords(keywords_file)

    ######## Needs Implementation ########
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

    ########## END - Needs Implementation ##########

    ########## Class methods that will be shared by all children ##########
    def flush_posts(self, filename, data):
        """Flush all the posts saved in the self.post Dataframe, and output to a file at the
        specified output directory. The output data will be structured using a pandas DataFrame to generate
        a csv file.

        Args:
            filename (str): full directory + filename where the file will be saved and data will be written to
        """

        data.to_csv(filename, sep="\t", index=False)
        print("[INFO] Data outputted to file: {}".format(filename))

    ######## Private Class Functions ########
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
