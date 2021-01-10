import mutagen
from music_config import PATH
import os


def parse(filename, ext):
    path = PATH + os.sep + filename + '.' + ext
    audio = mutagen.File(path)
    title = filename
    artist = filename
    album = filename
    
    if 'title' in audio:
        title = " ".join(audio['title'])
    if 'artist' in audio:
        artist = " ".join(audio['artist'])
    if 'album' in audio:
        album = " ".join(audio['album'])
        
    if 'TIT2' in audio:
        title = " ".join(audio['TIT2'].text)
    if 'TPE1' in audio:
        artist = " ".join(audio['TPE1'].text)
    if 'TALB' in audio:
        album = " ".join(audio['TALB'].text)

    res = {
        'title' : title,
        'artist' : artist,
        'album' : album
    }

    return res 