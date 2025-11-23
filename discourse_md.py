import urllib.parse
from http import HTTPStatus
from typing import Any

import requests
import requests.adapters
from typer import Typer
from urllib3 import Retry

app = Typer()


def get_session() -> requests.Session:
    """
    Mainly needed to ensure tests can run without hitting ``TOO_MANY_REQUESTS``.
    """
    retry_strategy = Retry(
        total=5,
        status_forcelist=[HTTPStatus.TOO_MANY_REQUESTS.value],
        backoff_factor=2,
    )

    adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


@app.command(help="Download a Discourse thread as markdown.")
def main_command(url: str) -> None:
    parsed = urllib.parse.urlparse(url)

    # `parsed_path` is like `/t/slug/topic_id/post_number`.
    parsed_path = parsed.path
    path_parts = parsed_path.strip("/").split("/")
    topic_id = path_parts[2]

    site = f"{parsed.scheme}://{parsed.netloc}"
    base_url = f"{site}/t/{topic_id}"

    # Fetch topic to get title and stream
    # Format is described at:
    # https://github.com/discourse/discourse_api_docs/blob/bb190ab5367fe5c5baf8b503dce952d1a2d4ab1d/openapi.yml#L7291-L7296
    # More readable:
    # https://docs.discourse.org/#tag/Topics/operation/getTopic
    topic_url = f"{base_url}.json?include_raw=true"
    session = get_session()
    response = session.get(topic_url)
    data: dict[str, Any] = response.json()

    title: str = data["title"]
    stream: list[int] = data["post_stream"]["stream"]
    posts_dict: dict[int, dict[str, Any]] = {
        p["id"]: p for p in data["post_stream"]["posts"]
    }

    # Fetch remaining posts individually
    for post_id in stream:
        if post_id in posts_dict:
            continue
        # https://docs.discourse.org/#tag/Posts/operation/getPost
        post_url = f"{site}/posts/{post_id}.json?include_raw=true"
        response = session.get(post_url)
        post_data: dict[str, Any] = response.json()
        posts_dict[post_id] = post_data

    # No idea if sorting is preserved, so sort it manually.
    posts = sorted(posts_dict.values(), key=lambda p: p["id"])

    print(f"# {title}")
    print()

    for post in posts:
        author = post["username"]
        created_at = post["created_at"]
        raw = post["raw"]
        print(f"## Post {post['post_number']} by {author} on {created_at}")
        print()
        print(raw)
        print()
        print("---")
        print()


# Separate function for `project.scripts`.
def main() -> None:
    app()


if __name__ == "__main__":
    main()
