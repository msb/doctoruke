import json, os, requests, urllib
from bs4 import BeautifulSoup


def main(opts):
    song_db = {}

    response = requests.get(opts['<doctoruke-url>'] + 'songs.html')
    if not response.ok:
        response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    for anchor in soup.find_all("a"):
        if anchor.get_text() != ' BAR':
            href = anchor.get('href')
            if href and href.endswith('.pdf'):
                onclick = anchor.get('onclick')
                if onclick:
                    onclick_parts = onclick.split("'")
                    if onclick_parts[0] == 'window.open(' and onclick_parts[1].endswith('.html'):
                        song_name = retrieve(opts, href, onclick_parts[1])
                        if song_name:
                            if song_name not in song_db:
                                song_db[song_name] = []
                            song_db[song_name].append(anchor.get_text().strip())

    with open(opts['--song-db'], 'w') as song_db_file:
        json.dump(song_db, song_db_file, sort_keys=True, indent=4)


def retrieve(opts, pdf, page):
    url = opts['<doctoruke-url>']
    song_name = pdf.split('.')[0]
    if song_name not in opts['--song-exclude'].split(','):
        pdf_local = opts['<pdf-dir>'] + pdf
        if not os.path.isfile(pdf_local):
            print(pdf_local)
            urllib.request.urlretrieve(url + pdf, pdf_local)

        song_local = opts['<song-dir>'] + song_name + '.mp3'
        if not os.path.isfile(song_local):
            response = requests.get(url + page)
            if not response.ok:
                response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            mp3 = None
            for script in soup.find_all("script"):
                if script.string:
                    for part in script.string.split('"'):
                        if part.endswith('.mp3'):
                            mp3 = part
            if not mp3:
                raise Exception("can't find mp3")
            urllib.request.urlretrieve(url + mp3, song_local)
            print(song_local)
        return song_name
    return None


