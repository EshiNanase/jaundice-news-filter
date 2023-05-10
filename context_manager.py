from contextlib import asynccontextmanager
from time import monotonic
import logging


@asynccontextmanager
async def count_analysis_duration(title):
    start = monotonic()
    try:
        yield
    finally:
        logging.info(f'{title} took {monotonic() - start}')
