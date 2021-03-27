"""
Tools to do various useful things with Dropbox.

Usage:
    doctoruke (-h | --help)
    doctoruke scrape [--verbose] [--song-page-cache=FILE] <doctoruke-url> <song-dir> <pdf-dir>
    doctoruke tag [--verbose] [--song-page-cache=FILE] [--tag-tracknumber=TAG]
              [--tag-album=TAG] [--tag-albumartist=TAG] [--tag-artist=TAG] <song-dir>

Options:
    -h, --help              Show a brief usage summary.
    -v, --verbose           Increase verbosity.

    <doctoruke-url>         The Doctor Uke URL.
    <song-dir>              The directory to save song tracks to.
    <pdf-dir>               The directory to save song PDFs to.

    --song-exclude=LIST     A comma seperated list of songs to exclude from the Dropbox directory.
    --song-page-cache=FILE  A JSON output file caching key data from each song page
                            [default: ./song-page-cache.json]
    --tag-tracknumber=TAG   Sets the TRACKNUMBER tag for a song track format "i,n"
                            where i is track and n is total track
    --tag-album=TAG         Sets the ALBUM tag for a song track
    --tag-albumartist=TAG   Sets the ALBUMARTIST tag for a song track
    --tag-artist=TAG        Sets the ARTIST tag for a song track

Sub commands:

    scrape  Scrapes the main page and retrieves all song tracks and PDFs.
    tag     Onced scraped, tags the song tracks, using the <song-db> for titles.

"""
import logging
import docopt
import asyncio


def main():
    opts = docopt.docopt(__doc__)
    logging.basicConfig(level=logging.INFO if opts['--verbose'] else logging.WARN)
    if opts['scrape']:
        from . import scrape
        asyncio.run(scrape.main(opts))
    if opts['tag']:
        from . import tag
        tag.main(opts)
