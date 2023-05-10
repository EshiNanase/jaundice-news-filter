from aiohttp import web
import logging
import aiohttp
from adapters.inosmi_ru import sanitize
from text_tools import split_by_words, calculate_jaundice_rate, fetch_charged_words
from anyio import create_task_group
import pymorphy2
from statuses import OK, FETCH_ERROR, PARSING_ERROR, TIMEOUT
from adapters.exceptions import ArticleNotFound
from aiohttp.client_exceptions import ClientError, InvalidURL
from asyncio.exceptions import TimeoutError
from async_timeout import timeout
from context_manager import count_analysis_duration


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def process_article(session, morph, charged_words, url, title, results, timeout_download=3, timeout_analysis=3):

    words_count = None
    score = None

    async with count_analysis_duration(title) as _:

        try:

            async with timeout(timeout_download):
                html = await fetch(session, url)

            humanized_html = sanitize(html)

            async with timeout(timeout_analysis):
                normalized_html = await split_by_words(morph, humanized_html)
                words_count = len(normalized_html)
                score = calculate_jaundice_rate(charged_words, normalized_html)
                status = OK

        except (ClientError, InvalidURL):
            status = FETCH_ERROR

        except ArticleNotFound:
            status = PARSING_ERROR

        except TimeoutError:
            status = TIMEOUT

    results[title] = {
        'url': url,
        'word_count': words_count,
        'score': score,
        'status': status,
    }


async def handle_index_page(request):
    params = request.rel_url.query
    urls = [url for url in params['urls'].split(',')]

    results = {}

    if len(urls) > 10:
        return web.json_response({"error": "too many urls in request, should be 10 or less"}, status=404)

    async with aiohttp.ClientSession() as session:
        async with create_task_group() as task_group:
            for article_index, article in enumerate(urls):
                task_group.start_soon(process_article, session, morph, charged_words, article, article_index, results)

    return web.json_response(results)


if __name__ == '__main__':

    app = web.Application()

    logging.basicConfig(level=logging.INFO)

    morph = pymorphy2.MorphAnalyzer()
    app['morph'] = morph

    charged_words = fetch_charged_words('negative_words.txt')
    app['charged_words'] = charged_words

    app.add_routes([web.get('/', handle_index_page)])
    web.run_app(app)
