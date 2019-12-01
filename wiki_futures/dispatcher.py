from concurrent.futures import as_completed

import requests
from requests_futures.sessions import FuturesSession

LIMIT = 500


class WikiDispatcher:
    def __init__(self, titles=None, num=None):
        self.num = num

        if titles:
            self.titles = titles

    def get_titles(self, num):
        params = {"rnnamespace": 0, "list": "random", "rnlimit": num, "format": "json"}

        random_resp = requests.get(f"http://en.wikipedia.org/w/api.php?action=query", params=params)
        random_data = random_resp.json()
        return [page["title"] for page in random_data["query"]["random"]]

    def parse_all(self, num=None):
        if not num:
            num = self.num
        if not num:
            raise ValueError("must provide at least one URL to scape")

        all_data = {}
        
        titles = self.get_titles(num)

        with FuturesSession() as session:
            query_params = {"prop": "extracts|revisions", "explaintext": "", "rvprop": "ids"}
            futures = [
                session.get(
                    f"https://en.wikipedia.org/w/api.php?format=json&action=query&titles={title}", params=query_params
                )
                for title in titles
            ]

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
