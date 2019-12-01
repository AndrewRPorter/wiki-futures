from concurrent.futures import as_completed

import requests
from requests_futures.sessions import FuturesSession

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "wiki-futures (https://github.com/AndrewRPorter/wiki-futures)"
MAX_WORKERS = 8

class WikiDispatcher:
    headers = {"User-Agent": USER_AGENT}
    def __init__(self, titles=None, num=None, workers=MAX_WORKERS):
        self.num = num
        self.workers = workers

        if titles:
            self.titles = titles

    def get_titles(self, num):
        """Queries a given random number of titles from Wikipedia"""
        params = {"rnnamespace": 0, "list": "random", "rnlimit": num, "format": "json", "action": "query"}

        random_resp = requests.get(f"{API_URL}", params=params, headers=self.headers)
        random_data = random_resp.json()
        return [page["title"] for page in random_data["query"]["random"]]

    def get_content(self, num=None, titles=None):
        """Queries a given number of Wikipedia pages asynchronously"""
        if not num:
            if not self.num and not titles:
                raise ValueError("must provide at least one URL to scape or provide a list of titles")
            else:
                num = self.num

        all_data = {}

        titles = titles if titles else self.get_titles(num)  # use custom titles to function

        with FuturesSession(max_workers=self.workers) as session:
            query_params = {"prop": "extracts", "explaintext": "", "rvprop": "ids", "format": "json", "action": "query"}
            futures = [session.get(f"{API_URL}?titles={title}", params=query_params, headers=self.headers) for title in titles]

            for future in as_completed(futures):
                resp = future.result()
                data = resp.json()
                page_id = list(data["query"]["pages"].keys())[0]
                title = data["query"]["pages"][page_id]["title"]

                if "extract" not in data["query"]["pages"][page_id]:
                    # TODO: more elegant way to handle this
                    print("couldn't get extract from:", title, page_id, data)
                    continue

                content = data["query"]["pages"][page_id]["extract"]
                all_data[title] = content

        return all_data
