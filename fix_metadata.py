from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error
import sys
import urllib.request

def main():
    if len(sys.argv) < 2:
        print('error: specify an argument')
        sys.exit(1)

    audio = MP3(sys.argv[1], ID3=ID3)
    u = urllib.request.urlretrieve('https://is5-ssl.mzstatic.com/image/thumb/Music60/v4/10/e8/19/10e8197e-d0cd-79b3-183d-d0d1e604a5db/source/100x100bb.jpg', 'cover.jpg')
    image_data = open('cover.jpg', 'rb').read()
    id3 = ID3(sys.argv[1])
    id3.add(APIC(3, 'image/jpeg', 3, 'Front Cover', image_data))
    id3.save(v2_version=3)

if __name__ == '__main__':
    main()
