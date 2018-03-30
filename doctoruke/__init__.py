"""
Tools to do various useful things with Dropbox.

Usage:
    doctoruke (-h | --help)
    doctoruke scrape [--verbose] [--song-exclude=LIST] [--output-db=FILE] <doctoruke-url> <song-dir> <pdf-dir>

Options:
    -h, --help            Show a brief usage summary.
    -v, --verbose         Increase verbosity.

    <doctoruke-url>       The Doctor Uke URL.
    <song-dir>            The directory to save song tracks to.
    <pdf-dir>             The directory to save song PDFs to.

    --song-exclude=LIST   A comma seperated list of songs to exclude from the Dropbox directory.
    --output-db=FILE      A JSON output file mapping file names to song titles [default: ./doctoruke.json]

Sub commands:

    scrape  Scrapes the main page and retrieves all song tracks and PDFs.

"""
import logging
import docopt

def main():
    opts = docopt.docopt(__doc__)
    logging.basicConfig(level=logging.INFO if opts['--verbose'] else logging.WARN)
    if opts['scrape']:
        from . import scrape
        scrape.main(opts)

