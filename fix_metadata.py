"""
fix_metadata.py -- fixed metadata of mp3 files

"""


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
    return escape(file_name).replace(' ', '+')


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


if __name__ == '__main__':
    main()
