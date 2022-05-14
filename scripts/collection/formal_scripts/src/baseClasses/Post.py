from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Post(ABC):
  """Post will act as a data class for abstracting data storage for post data. 
  This includes Post titles, text content, responses, digital media, and others.
  Can be expanded upon by creating new subclasses that add more specific data storage items if needed.
  """

  title: str
  author: str
  post_content: str
  replies: dict[str,str]
  # Can add other data points in subclasses based on needs of the website

  @abstractmethod
  def to_str(self):
    """Method for converting the data item into a parse-able string format for saving to file
    eventually. This will automatically format this object's contents to the desired output
    format (ie. JSON, CSV, etc.)
    """
    pass