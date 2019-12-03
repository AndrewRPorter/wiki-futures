import pytest

from wiki_futures import dispatcher

TEST_NUM_PAGES = 10
BOT_MAX_RNLIMIT = 5001


def test_valid_titles():
    titles = dispatcher.get_titles(TEST_NUM_PAGES)
    assert len(titles) == TEST_NUM_PAGES
    assert len(set(titles)) == TEST_NUM_PAGES  # make sure no duplicates exist


def test_large_titles():
    titles = dispatcher.get_titles(BOT_MAX_RNLIMIT + 1)
    assert len(titles) == BOT_MAX_RNLIMIT + 1


def test_content_size():
    results = dispatcher.get_content(TEST_NUM_PAGES)
    assert len(results) == TEST_NUM_PAGES


def test_content_titles():
    titles = ["Python", "Wikipedia"]
    results = dispatcher.get_content(titles=titles)
    assert len(results) == len(titles)


def test_bad_content_params():
    with pytest.raises(ValueError):
        dispatcher.get_content()


def test_bad_content_titles():
    bad_title = ["bad_query"]  # this should almost always be a bad query
    with pytest.warns(None) as record:
        results = dispatcher.get_content(titles=bad_title)
    assert len(record) == 1
