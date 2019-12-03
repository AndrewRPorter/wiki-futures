import warnings
from concurrent.futures import as_completed

import requests
from requests_futures.sessions import FuturesSession

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "wiki-futures (https://github.com/AndrewRPorter/wiki-futures)"
MAX_WORKERS = 8

headers = {"User-Agent": USER_AGENT}


def get_titles(num):
    """Queries a given random number of titles from Wikipedia"""
    params = {"rnnamespace": 0, "list": "random", "rnlimit": num, "format": "json", "action": "query"}

    random_resp = requests.get(f"{API_URL}", params=params, headers=headers)
    random_data = random_resp.json()
    return [page["title"] for page in random_data["query"]["random"]]


def get_content(num=0, workers=8, titles=None):
    """Queries a given number of Wikipedia pages asynchronously"""
    if num <= 0 and not titles:
        raise ValueError("num must be greater than zero if no titles passed in")

    if not titles:
        titles = get_titles(num)  # use custom titles if provided

    num_workers = workers

    all_data = {}

    with FuturesSession(max_workers=num_workers) as session:
        query_params = {"prop": "extracts", "explaintext": "", "format": "json", "action": "query"}
        futures = [session.get(f"{API_URL}?titles={title}", params=query_params, headers=headers) for title in titles]

        for future in as_completed(futures):  # add data to dictionary when futures complete
            resp = future.result()
            data = resp.json()

            page_id = list(data["query"]["pages"].keys())[0]  # page_id not accessible without iteration over page keys
            title = data["query"]["pages"][page_id]["title"]

            if page_id == "-1":  # title yielded a bad page query
                warnings.warn(f"unable to get valid page for '{title}'", RuntimeWarning)
            else:
                content = data["query"]["pages"][page_id]["extract"]
                all_data[title] = content

    return all_data
