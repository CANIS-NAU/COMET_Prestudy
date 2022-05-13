# imports
from ...baseClasses.Post import Post
from dataclasses import dataclass

@dataclass
class GooglePost(Post):
  media: list[bytes]

  def to_str(self):
    """TODO converts post items into \n separated values, 
    Will be changed when actual output format is decided
    """
    return f'Title: {self.title}\nContent: {self.post_content}\nReplies: {self.replies}\nMedia: #{len(self.media)} Media items were found\n\n'
