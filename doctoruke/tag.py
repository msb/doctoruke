import json, eyed3


def main(opts):

    with open(opts['--song-db']) as song_db_file:
        song_db = json.load(song_db_file)

    for song_name, song_titles in song_db.items():
        song = eyed3.load(f'{opts["<song-dir>"]}/{song_name}.mp3').tag
        if song.title != song_titles[0]:
            song.title = song_titles[0]
            print(song_titles[0])
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

