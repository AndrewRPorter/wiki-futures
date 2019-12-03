wiki-futures
------------

Uses python [requests_futures](https://github.com/ross/requests-futures) to asynchronously download Wikipedia pages.

Installation
------------

`pip3 install --user wiki-futures`

Usage
-----

Get 10 random wikipedia articles

```python
from wiki_futures import dispatcher
content = dispatcher.get_content(10)
```

If you want to pass in custom titles you can do so like this

```python
content = dispatcher.get_content(titles=["Python", "GitHub"])
```

Pass in workers value to change the default, which is 8
```python
from wiki_futures import dispatcher
content = dispatcher.get_content(10, workers=4)
```

Get list of random titles. This is helpful because the limit for non-bots is 500.
```python
from wiki_futures import dispatcher
titles = dispatcher.get_titles(1000)
```


Motivation
----------

Most of my NLP projects revolved around download random wikipedia articles, I wanted a quick way to download them
concurrently and I found the python wikipedia package to be too cumbersome to work around.