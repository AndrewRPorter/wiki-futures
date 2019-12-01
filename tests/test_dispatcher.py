import pytest

from wiki_futures.dispatcher import WikiDispatcher

TEST_NUM_PAGES = 10


def test_titles():
    dispatcher = WikiDispatcher()
    titles = dispatcher.get_titles(TEST_NUM_PAGES)
    assert len(titles) == TEST_NUM_PAGES
    assert len(set(titles)) == TEST_NUM_PAGES  # make sure no duplicates exist


def test_results_size():
    dispatcher = WikiDispatcher()
    results = dispatcher.parse_all(TEST_NUM_PAGES)
    assert len(results) == TEST_NUM_PAGES


def test_bad_params():
    dispatcher = WikiDispatcher()
    with pytest.raises(ValueError):
        dispatcher.parse_all()
