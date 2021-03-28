# Doctor Uke Tools

A set of tools to help me retrieve song resources (PDFs and audio) from the awesome
(http://www.doctoruke.com).

## Getting Started

Create a virtual environment (a one-off command):

```
virtualenv -p python3.8 .venv
```

Activate the virtual environment (run for every new session):

```
source .venv/bin/activate
```

Install the requirements from the setup.py (a one-off command):

```
pip install -e .
```

You should now be able to run the command:

```
doctoruke --help
```

## Examples

### Scraping & Tagging

The "scrape" command scrapes the main page and retrieves all song tracks and PDFs.
I normally do this with the following command:

```
doctoruke scrape http://www.doctoruke.com "$DOCTORUKE_PDFS" "$DOCTORUKE_AUDIO"
```

To minimise requests to the website the process saves key page data in file called
`song-page-cache.json`. If necessary, the downloading of a particular file can be supressed by
pre-pending it with "!". Eg:

```
    :
    "/_player/addamsfamily.html": [
        "Addams Family Theme",
        "addamsfamily",
        "!addamsfamily"
    ],
    :
```

Once scraped the "tag" command tags the song tracks, using the song page cache file created
previously for titles. I normally to this with the following command:

```
doctoruke tag --tag-tracknumber=, --tag-album='The Complete Doctor Uke' \
  --tag-albumartist='Doctor Uke' --tag-artist='Doctor Uke' "$DOCTORUKE_AUDIO"
```
