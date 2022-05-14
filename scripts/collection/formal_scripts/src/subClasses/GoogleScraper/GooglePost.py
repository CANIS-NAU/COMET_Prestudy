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

    newline = '\n'
    tab= '\t'

    return f'Title: {self.title}\n' + \
            'Content: ' + self.post_content.replace("\n", " ") + '\n' + \
            'Replies:\n' + "\n".join(f"{tab}{author}: {reply.replace(newline, ' ')}" for author, reply in self.replies.items()) + \
            f'Media: {len(self.media) if self.media else 0} Media items were found\n\n'
