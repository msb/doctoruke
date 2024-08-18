import logging
import os
import re
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

LOGGER = logging.getLogger(__name__)

# doctoruke's main index
INDEX_PAGE = 'songs.html'

# the doctoruke url path for all audio files
SONGS_PATH = '_player/_songs/'

# used to match for the index page's song page anchors
HREF_REGEX = r'\/_player\/.*\.html'

# used to extract the song title and file names from a song page
SCRIPT_REGEX = (
    r'.*var songTitle = "(.*?)";.*?var pdfName = "(.*?)";.*?var audioFileName = "(.*?)";.*'
)

# the max number of IO tasks to process concurrently
MAX_CONCURRENT_TASKS = 3


async def worker(queue):
    """
    A worker method that continually de-queues tasks and executes them
    """
    while True:
        # get an IO task out of the queue
        awaitable = await queue.get()

        await awaitable

        # notify the queue that the IO task has been processed.
        queue.task_done()


async def main(opts):
    """
    Scrapes the main page and retrieves all song tracks and PDFs.
    """

    # loads the song page cache
    try:
        with open(opts['--song-page-cache'], 'r') as song_page_cache_file:
            song_page_cache = json.load(song_page_cache_file)
    except FileNotFoundError:
        song_page_cache = {}

    # create a queue that we will use to store our tasks
    queue = asyncio.Queue()

    # create a set of worker tasks to process the queue concurrently
    tasks = [asyncio.create_task(worker(queue)) for i in range(MAX_CONCURRENT_TASKS)]

    async with httpx.AsyncClient() as client:

        # reads all new song pages linked in song index page and adds them to the song page cache

        LOGGER.info('scan index for updates..')

        for song_page in new_song_pages(opts, song_page_cache):
            queue.put_nowait(
                read_page(opts['<doctoruke-url>'], song_page_cache, client, song_page)
            )

        await queue.join()

        # iterates over the song page cache and retrieves all new song files

        LOGGER.info('retrieve new song files..')

        for remote_url, local_path in new_song_files(opts, song_page_cache):
            queue.put_nowait(get_new_file(client, remote_url, local_path))

        await queue.join()

    # saves the song page cache
    with open(opts['--song-page-cache'], 'w') as song_page_cache_file:
        json.dump(song_page_cache, song_page_cache_file, sort_keys=True, indent=4)

    # cancel our worker tasks and wait until they are cancelled
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


def new_song_pages(opts, song_page_cache):
    """
    Generator that parses the song index page and yields all song page paths not already in the
    song page cache.
    """
    response = httpx.get(urljoin(opts['<doctoruke-url>'], INDEX_PAGE))
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    for anchor in soup.find_all("a"):
        href = urlparse(anchor.get('href'))
        if href.query != 'bar=1':
            song_page = str(href.path)
            song_page_match = re.match(HREF_REGEX, song_page)
            if song_page_match and song_page not in song_page_cache:
                yield song_page


def new_song_files(opts, song_page_cache):
    """
    Generator that iterates over the song page cache and yields all names of files not already
    downloaded.
    """
    songs_url = urljoin(opts['<doctoruke-url>'], SONGS_PATH)

    for _, pdf_base, mp3_base in song_page_cache.values():
        yield from new_song_file(pdf_base + '.pdf', opts['<pdf-dir>'], opts['<doctoruke-url>'])
        yield from new_song_file(mp3_base + '.mp3', opts['<song-dir>'], songs_url)


def new_song_file(file_name, local_folder, remote_url):
    """
    Generator that yields the name of a file not already downloaded. Also ignores if the file name
    starts with a "!".
    """
    if not file_name.startswith('!'):
        file_path = os.path.join(local_folder, file_name)
        if not os.path.isfile(file_path):
            yield urljoin(remote_url, file_name), file_path


async def read_page(doctoruke_url, song_page_cache, client, song_page):
    """
    Downloads a song page, parses song data from the page's script tags (title and file names), and
    adds the data to the song page cache.
    """
    try:
        response = await client.get(urljoin(doctoruke_url, song_page))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup.find_all("script"):
            if script.string:
                match = re.match(SCRIPT_REGEX, script.string, re.DOTALL)
                if match:
                    song_page_data = match.groups()
                    song_page_cache[song_page] = song_page_data
                    break
        LOGGER.info(song_page)
    except httpx.HTTPError as e:
        LOGGER.error('failed:' + song_page)
        song_page_cache[song_page] = (str(e), '!unknown', '!unknown')


async def get_new_file(client, remote_url, local_path):
    """
    Downloads a song file from Doctor Uke.
    """
    try:
        with open(local_path, 'wb') as f:
            async with client.stream('GET', remote_url) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
        LOGGER.info(local_path)
    except httpx.HTTPError as e:
        LOGGER.error(f'{local_path} failed: {e}')
        os.remove(local_path)
