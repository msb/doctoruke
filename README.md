# Doctor Uke Tools

Tools to help me retrieve song resources from the awesome (http://www.doctoruke.com).

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
doctoruke scrape --song-exclude=incrowdc,beautifulfreamer http://www.doctoruke.com/ "$CLOUD/Music/Library/0.Doctor Uke/" "$CLOUD/Documents/Songbooks/Doctor Uke/"
```

Once scraped the "tag" command tags the song tracks, using the <song-db> for titles.
I normally to this with the following command:

```
doctoruke tag --tag-tracknumber=, --tag-album='The Complete Doctor Uke' --tag-albumartist='Doctor Uke' --tag-artist='Doctor Uke' "$CLOUD/Music/Library/0.Doctor Uke/"
```

