from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

class WikiDispatcher:
    def __init__(self, num=None):
        self.num = num

    def parse_all(self, num=None):
        if not num:
            num = self.num
        if not num:
            raise ValueError("must provide at least one URL to scape")

        with FuturesSession() as session:
            futures = [session.get("https://en.wikipedia.org/wiki/Special:Random") for _ in range(0, num)]

            for future in as_completed(futures):
                resp = future.result()
                print(resp.content)
