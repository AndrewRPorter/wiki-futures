wiki-futures
------------

Uses python `requests_futures` to asynchronously download Wikipedia pages.

Installation
------------

`pip3 install --user wiki-futures`

Usage
-----

```python
from wiki_futures.dispatcher import WikiDispatcher
dispatcher = WikiDispatcher(num=10)
all_content = dispatcher.parse_all()
```

If you don't know how many pages you want to get on initialization, you can create the dispatcher like this:

```python
from wiki_futures.dispatcher import WikiDispatcher
dispatcher = WikiDispatcher()
all_content = dispatcher.parse_all(num=10)
```

Motivation
----------

Most of my NLP projects revolved around download random wikipedia articles, I wanted a quick way to download them
concurrently and I found the python wikipedia package to be too cumbersome to work around.