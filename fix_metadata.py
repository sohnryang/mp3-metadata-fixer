"""
fix_metadata.py -- fixed metadata of mp3 files

"""


import shutil
import sys
import requests
from xml.sax.saxutils import escape
from mutagen.id3 import ID3, APIC


def generate_search_query(file_name):
    """
    generate_search_query(flie_name: str) -- generate a search query which is
    fed to iTunes API.

    Arguments:
    file_name: str -- name of a file which is used to generate a query.
    """
    return escape(file_name).replace(' ', '+').replace('.mp3', '')


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


def download_cover_image(url, file_name):
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


if __name__ == '__main__':
    main()
