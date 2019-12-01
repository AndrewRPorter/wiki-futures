import pytest

from wiki_futures.dispatcher import WikiDispatcher


def test_results_size():
    dispatcher = WikiDispatcher()
    results = dispatcher.parse_all(10)
    assert len(results) == 10
