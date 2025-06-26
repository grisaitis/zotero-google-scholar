import logging
import os
import urllib.parse
from pprint import pprint

from dotenv import load_dotenv
from pyzotero import zotero
from scholarly import scholarly

load_dotenv()

logger = logging.getLogger(__name__)

# Zotero API setup
library_id = os.getenv("ZOTERO_LIBRARY_ID")  # Your Zotero user ID
api_key = os.getenv("ZOTERO_API_KEY")  # Your Zotero API key
library_type = "user"  # or 'group'


def print_collections():
    zot = zotero.Zotero(library_id, library_type, api_key)
    collections = zot.collections()
    for collection in collections:
        print(f'"{collection["data"]["key"]}",  # "{collection["data"]["name"]}"')


def print_items(collection_key: str):
    """Print all items in a Zotero collection."""
    zot = zotero.Zotero(library_id, library_type, api_key)
    collection = zot.collection(collection_key)
    items = zot.collection_items_top(collection["data"]["key"])
    for item in items:
        print(
            f'"{item["data"]["key"]}",  # "{item["data"].get("title", "(No title)")}"'
        )


def print_item(item_key: str):
    zot = zotero.Zotero(library_id, library_type, api_key)
    item = zot.item(item_key)
    pprint(item)


def print_child_items(zotero_item_key: str):
    """Print all attachments of a Zotero item."""
    zot = zotero.Zotero(library_id, library_type, api_key)
    child_items = zot.children(zotero_item_key)
    pprint(child_items, indent=2)


def has_google_scholar_attachment(item_key: str) -> bool:
    """Check if a Zotero item has a Google Scholar attachment."""
    zot = zotero.Zotero(library_id, library_type, api_key)
    child_items = zot.children(item_key)
    for child_item in child_items:
        if item_is_google_scholar_link(child_item):
            return True
    return False


def item_is_google_scholar_link(zotero_item: dict) -> bool:
    item_data = zotero_item["data"]
    try:
        url = item_data["url"]
    except KeyError:
        return False
    return url.startswith("https://scholar.google.com/")


def get_items(collection):
    zot = zotero.Zotero(library_id, library_type, api_key)
    items = zot.collection_items_top(collection["data"]["key"])
    return items


def add_google_scholar_link_to_item(zotero_item_key: str):
    zot = zotero.Zotero(library_id, library_type, api_key)
    zotero_item = zot.item(zotero_item_key)
    title = zotero_item["data"].get("title", "")
    url = create_scholar_search_url(title)
    add_link_to_item(zotero_item_key, url, "Google Scholar")


def add_google_scholar_links(collection_key: str):
    zot = zotero.Zotero(library_id, library_type, api_key)
    items = zot.collection_items_top(collection_key)
    for item in items:
        item_key = item["data"]["key"]
        logger.info("processing item %s", item_key)
        if item_is_google_scholar_link(item):
            logger.info("skipping, is a Google Scholar link")
            continue
        if has_google_scholar_attachment(item_key):
            logger.info("skipping, already has a Google Scholar link")
            continue
        title = item["data"].get("title", "")
        if not title:
            logger.info("skipping, no title")
            continue
        url = create_scholar_search_url(title)
        logger.info("adding google scholar link, url: %s", url)
        add_link_to_item(item_key, url, "Google Scholar")


def demo():
    zot = zotero.Zotero(library_id, library_type, api_key)
    # items = zot.top(limit=1)
    collections = [
        # "4S6WU66T",  # "AI optimization"
        # "LDERK2V5",  # "multimodal AI systems"
        "3KXE4D7B",  # "AI for computer control"
        # "LHL2DQVX",  # "AI for Statistical Reasoning"
        # "MZ2QZ8ZD",  # "LLMs for tabular"
        # "IGFKKWLF",  # "prompt optim"
        # "QU59YEI2",  # "cs224n"
        # "NDU5W7DM",  # "transformer architectures"
        # "78XST3VM",  # "compound AI"
    ]
    collections = zot.collections()
    for collection in collections:
        print_items(collection["data"]["key"])
        break


def add_link_to_item(zotero_item_key: str, link_url: str, link_title: str):
    zot = zotero.Zotero(library_id, library_type, api_key)
    attachment_data = {
        "itemType": "attachment",
        "linkMode": "linked_url",
        "url": link_url,
        "title": link_title,
        "parentItem": zotero_item_key,
    }
    zot.create_items([attachment_data])


def create_scholar_search_url(title, authors: list[str] = []) -> str:
    query = f"{title} {' '.join(authors)}"
    encoded_query = urllib.parse.quote_plus(query)
    return f"https://scholar.google.com/scholar?q={encoded_query}"


def get_scholar_first_search_result(search_query: str):
    search_result = scholarly.search_pubs(search_query)
    first_result = next(search_result, None)
    if first_result:
        return first_result
    else:
        return None
