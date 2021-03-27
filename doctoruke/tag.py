import os
import json
import eyed3


def main(opts):
    """
    """
    with open(opts['--song-page-cache']) as song_page_cache_file:
        song_page_cache = json.load(song_page_cache_file)

    for song_title, _, song_name in song_page_cache.values():
        if not song_name.startswith('!'):
            song = eyed3.load(os.path.join(opts['<song-dir>'], song_name + '.mp3')).tag
            if song.title != song_title:
                song.title = song_title
                print(song_title)
                if '--tag-tracknumber' in opts:
                    track_num = opts['--tag-tracknumber'].split(',')
                    song.track_num = (none(track_num[0]), none(track_num[1]))
                if '--tag-album' in opts:
                    song.album = none(opts['--tag-album'])
                if '--tag-albumartist' in opts:
                    song.album_artist = none(opts['--tag-albumartist'])
                if '--tag-artist' in opts:
                    song.artist = none(opts['--tag-artist'])
                song.save()


def none(value):
    return value if value else None
