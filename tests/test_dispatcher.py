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
    results = dispatcher.get_content(TEST_NUM_PAGES)
    assert len(results) == TEST_NUM_PAGES


def test_results_titles():
    titles = ["Python", "Wikipedia"]
    dispatcher = WikiDispatcher()
    results = dispatcher.get_content(titles=titles)
    assert len(results) == len(titles)


def test_bad_params():
    dispatcher = WikiDispatcher()
    with pytest.raises(ValueError):
        dispatcher.get_content()


def test_bad_titles():
    bad_title = ["bad_query"]  # this should almost always be a bad query
    dispatcher = WikiDispatcher()
    with pytest.warns(None) as record:
        results = dispatcher.get_content(titles=bad_title)
    assert len(record) == 1
