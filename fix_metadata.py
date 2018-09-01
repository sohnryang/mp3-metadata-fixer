"""
fix_metadata.py -- fix metadata of mp3 files

"""


import os
import shutil
import sys
import urllib.parse
import requests
from mutagen.id3 import ID3, APIC, TPE1, TALB, TRCK, TIT2


def generate_search_query(file_name):
    """
    generate_search_query(flie_name: str) -- generate a search query which is
    fed to iTunes API.

    Arguments:
    file_name: str -- name of a file which is used to generate a query.
    """
    raw_name = os.path.basename(file_name).replace('.mp3', '')
    return urllib.parse.quote(raw_name)


def get_itunes_search_results(query):
    """
    get_itunes_search_results(query: str) -- search for info of a music file
    via iTunes Web API.

    Arguments:
    query: str -- the query to search for info.
    """
    url = 'https://itunes.apple.com/search?term={0}'.format(query)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def download_cover_image(url, file_name='cover.jpg'):
    """
    download_cover_image(url: str, file_name: str) -- download the cover image
    from the given url.

    Arguments:
    url: str -- the url to download the image from.
    file_name: str -- the name of the file to download to.
    """
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(file_name, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def extract_first_result(search_result):
    """
    extract_first_result(search_result: dict) -- extract first result from
    iTunes search results.
    """
    return search_result['results'][0]


def fix_metadata(file_name, search_result):
    """
    fix_metadata(file_name: str, search_result: dict) -- fix mp3 file's
    metadata with search result.

    Arguments:
    file_name: str -- name of the mp3 file.
    search_result: dict -- a search result dict extracted from raw data.
    """
    audio = ID3(file_name)
    audio['TPE1'] = TPE1(encoding=3, text=search_result['artistName'])
    audio['TIT2'] = TIT2(encoding=3, text=search_result['trackName'])
    audio['TRCK'] = TRCK(encoding=3, text=str(search_result['trackNumber']))
    audio['TALB'] = TALB(encoding=3, text=search_result['collectionName'])
    audio.save()


def update_cover(file_name, cover_img_name='cover.jpg'):
    """
    update_cover(file_name: str, cover_img_name: str) -- update the file's
    cover image.

    Arguments:
    file_name: str -- name of the mp3 file.
    cover_img_name: str -- name of the cover file. (default: cover.jpg)
    """
    audio = ID3(file_name)
    with open(cover_img_name, 'rb') as img:
        audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3,
                             desc='Cover', data=img.read())
    audio.save()


def main():
    """
    main() -- main function

    """
    if len(sys.argv) < 2:
        print('fix_metadata: error: no file specified', file=sys.stderr)
        sys.exit(1)

    file_names = sys.argv[1:]
    for file_name in file_names:
        query = generate_search_query(file_name)
        search_result = get_itunes_search_results(query)
        first_result = extract_first_result(search_result)
        cover_image_url = first_result['artworkUrl100']
        download_cover_image(cover_image_url)
        update_cover(file_name)
        fix_metadata(file_name, first_result)


if __name__ == '__main__':
    main()
