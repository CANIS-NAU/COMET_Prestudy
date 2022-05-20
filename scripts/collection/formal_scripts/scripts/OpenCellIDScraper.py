# imports
from dataclasses import dataclass
from BaseScraper import Scraper, DriverType, Post
import json, requests 

# Post definitions
@dataclass
class OCellIDPost(Post):

    # TODO
    def to_str(self):
        """Convert data stored within the Post object into a string.
        This string will be used for data output to file later.
        """
        raise NotImplementedError


# Scraper definitions
class OCellIDScraper(Scraper):
    """Scraper object that specifically handles the OpenCellID forums (community.opencellid.org/)

    This Scraper object will make use of Discourse's REST API for fetching JSON files from the server
    This will make use of special URL syntax that will grab the required data from each search query as
    well as each selected post.

    **Getting all replies from within in a selected topic (including original post):**
    ``https://community.opencellid.org/t/{**topic_id**}.json?print=true``
    """

    def __init__(self, base_url: str, keywords_file: str, driver: DriverType):
        super().__init__(base_url, keywords_file, driver)

    # TODO
    def _collect_page_metadata(self, post_metadata_json) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated (within this object) and
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }

        Helper functions can be declared inside this method in order to keep things
        organized, but its no biggie.
        """

        # TODO
        def get_title():
            raise NotImplementedError

        # TODO
        def get_responses():
            raise NotImplementedError

        # TODO
        def get_post_content():
            raise NotImplementedError

        raise NotImplementedError

    def _find_posts(self, search_json) -> list[int]:
        """Provided a list of posts after a search query, parse the search JSON
        and return the IDs of all the resulting posts from the search.
        
        Parameters
        ----------
        search_json : dict
            The JSON result returned after conducting a :func:`~OCellIDScraper.search()` operation

        Returns
        -------
        list[str]
            A list of IDs for each identified post
        """

        posts = [topic['id'] for topic in search_json['topics']]
        return posts

    # TODO
    def _new_post(self, keyword: str):
        """With the help of the _collect_page_metadata function,
        gather the post data, then place the data into the appropriate
        fields within a respective Post subclass

        Parameters
        ----------
        keyword : str
            The search term that was used to obtain this post as a result
        """
        raise NotImplementedError

    def search(self, search_term: str):
        """Using the Discourse URL API, this function will send a get request to the
        OpenCellID forum website, and return a JSON document with the post IDs from 
        the resulting query. This JSON document can then be returned and parsed based on
        what data is required.

        **Getting all posts as a result of a keyword search:**
        ``https://community.opencellid.org/search.json?q={**keyword**}``

        Parameters
        ----------
        search_term : str
            The keyword/search-term you wish to query the website for
        """

        open_cell_id_query_url = self.base_url + "search.json?q=" + search_term
        return requests.get(open_cell_id_query_url).json()
