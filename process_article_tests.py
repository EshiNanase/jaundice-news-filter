import pytest
import pymorphy2
from text_tools import fetch_charged_words
from server import process_article
import aiohttp
from statuses import OK, FETCH_ERROR, PARSING_ERROR, TIMEOUT

VALID_URL = 'https://inosmi.ru/20230510/mozg-262714201.html'
FETCH_ERROR_URL = 'example.123'
PARSING_ERROR_URL = 'https://lotr.fandom.com/ru/wiki/%D0%A5%D1%80%D0%BE%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F'
TIMEOUT_ERROR_URL = 'https://inosmi.ru/20230510/mozg-262714201.html'


@pytest.mark.asyncio
async def test_process_article_ok():

    morph = pymorphy2.MorphAnalyzer()
    charged_words = fetch_charged_words('negative_words.txt')
    results = {}
    async with aiohttp.ClientSession() as session:
        await process_article(session, morph, charged_words, VALID_URL, 1, results)
        assert results == {
            1: {
                'url': VALID_URL,
                'word_count': 317,
                'score': 0.88,
                'status': OK
            }
        }


@pytest.mark.asyncio
async def test_process_article_fetch_error():

    morph = pymorphy2.MorphAnalyzer()
    charged_words = fetch_charged_words('negative_words.txt')
    results = {}
    async with aiohttp.ClientSession() as session:
        await process_article(session, morph, charged_words, FETCH_ERROR_URL, 1, results)
        assert results == {
            1: {
                'url': FETCH_ERROR_URL,
                'word_count': None,
                'score': None,
                'status': FETCH_ERROR
            }
        }


@pytest.mark.asyncio
async def test_process_article_parsing_error():

    morph = pymorphy2.MorphAnalyzer()
    charged_words = fetch_charged_words('negative_words.txt')
    results = {}
    async with aiohttp.ClientSession() as session:
        await process_article(session, morph, charged_words, PARSING_ERROR_URL, 1, results)
        assert results == {
            1: {
                'url': PARSING_ERROR_URL,
                'word_count': None,
                'score': None,
                'status': PARSING_ERROR
            }
        }


@pytest.mark.asyncio
async def test_process_article_timeout_error():

    morph = pymorphy2.MorphAnalyzer()
    charged_words = fetch_charged_words('negative_words.txt')
    results = {}
    async with aiohttp.ClientSession() as session:
        await process_article(session, morph, charged_words, TIMEOUT_ERROR_URL, 1, results, timeout_download=0.1)
        assert results == {
            1: {
                'url': TIMEOUT_ERROR_URL,
                'word_count': None,
                'score': None,
                'status': TIMEOUT
            }
        }
