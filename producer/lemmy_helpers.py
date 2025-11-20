import logging

from dataclasses import dataclass, field
from collections import deque
from tenacity import retry, wait_exponential
from pythorhead import Lemmy


logger = logging.getLogger(__name__)


@dataclass
class PostsIter:
    lemmy: Lemmy
    community_id: int
    current_page: int = 1
    limit: int = 50
    _posts_buffer: deque = field(default_factory=deque)

    @retry(
        stop=lambda state: state.attempt_number >= 3,
        wait=wait_exponential(min=4, max=10),
        reraise=True,
    )
    def _get_posts(self):
        logger.info(f"Fetching posts page={self.current_page} limit={self.limit}")
        return self.lemmy.post.list(
            community_id=self.community_id,
            page=self.current_page,
            limit=self.limit,
        )

    def __iter__(self):
        return self

    def __next__(self):
        if not self._posts_buffer:
            posts = self._get_posts()
            if not posts:
                logger.info("No more posts.")
                raise StopIteration
            self._posts_buffer.extend(posts)
            self.current_page += 1
        return self._posts_buffer.popleft()


def fetch_posts(
    username: str,
    password: str,
    lemmy_node: str,
    community_name: str,
    page: int = 1,
    limit: int = 50,
    buffer_size: int = 30
) -> iter:
    lemmy = Lemmy(lemmy_node)
    lemmy.log_in(username, password)
    logger.info(f"Logged in as {username}")

    community_id = lemmy.discover_community(community_name)
    logger.info(f"Discovered community '{community_name}', id={community_id}")

    posts_iter = PostsIter(lemmy, community_id, page, limit)

    buffer = []
    for post in posts_iter:
        post_info = post["post"]
        counts_info = post["counts"]

        post_entry = {
            "id": post_info["id"],
            "title": post_info["name"],
            "upvotes": counts_info["upvotes"],
        }

        buffer.append(post_entry)

        if len(buffer) >= buffer_size:
            for entry in buffer:
                yield entry
            logger.info(f"Fetched batch of {len(buffer)} posts.")
            buffer.clear()

    if buffer:
        for entry in buffer:
            yield entry
        logger.info(f"Fetched final batch of {len(buffer)} posts.")
