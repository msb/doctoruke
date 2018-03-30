# Doctor Uke Tools

Tools to help me retrieve song resources from the awesome (http://www.doctoruke.com).

## Getting Started

Create a virtual environment (a one-off command):

```
virtualenv -p python3.6 venv
```

To support music file tagging install the following library (a one-off command):

```
sudo apt-get install libtag1-dev
```

Activate the virtual environment (run for every new session):

```
source venv/bin/activate
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

### Scraping

The main tool scrapes the main page and retrieves all song tracks and PDFs.
I normally to this can be done with the following command:

```
doctoruke scrape --song-exclude=incrowdc http://www.doctoruke.com/ "$HOME/Music/Library/0.Doctor Uke/" "$HOME/Documents/Songbooks/Doctor Uke/"
```

