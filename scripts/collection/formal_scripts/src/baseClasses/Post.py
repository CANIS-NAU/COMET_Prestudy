from dataclasses import dataclass

@dataclass
class Post:
  """Post will act as a data class for abstracting data storage for post data. 
  This includes Post titles, text content, responses, digital media, and others.
  Can be expanded upon by creating new subclasses that add more specific data storage items if needed.
  """

  title: str
  content: str
  responses: str 
  media: bytes
  # Can add other data points in subclasses based on needs of the website