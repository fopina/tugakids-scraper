#!/usr/bin/env python3
import requests
from lxml import etree
from pathlib import Path
from tqdm import tqdm

# FIXME: move all these to argparse and default values
# taken from https://www.tugakids.com/kodi-spmc/ @ _Edit.py
MAIN_URL = 'http://bit.ly/2FCdP2F'
VIDEOS = Path('videos')
NFO_TEMPLATE = 'https://www.imdb.com/title/%(ttid)s'


def n2d(node):
    return {
        e.tag: e.text
        for e in node
    }


def parse_channels(doc):
    channels = doc.findall('.//channel')
    for channel in channels:
        yield n2d(channel)


def main():
    r = requests.get(MAIN_URL)
    r.encoding = r.apparent_encoding
    parser = etree.XMLParser(recover=True)
    xml = '<xml>' + r.text + '</xml>'

    channels = list(parse_channels(etree.fromstring(xml, parser=parser)))
    with tqdm(channels, desc='Scraping') as pb:
        errors = 0
        for channel in pb:
            name = channel['name'].strip()
            pb.set_postfix(name=name, errors=errors, refresh=False)
            strm = VIDEOS / f'{name}.strm'
            nfo = VIDEOS / f'{name}.nfo'
            if channel['thumbnail'] in ('http://tkimage23.buzz/last.jpg', 'http://tkimage23.buzz/icon.jpg'):
                continue
            try:
                er = requests.get(channel['externallink'])
                er.raise_for_status()
                er.encoding = er.apparent_encoding
                root = etree.fromstring(er.content, parser=parser)
                ed = n2d(root)
                strm.write_text(ed['link'])
                ttid = channel['externallink'].split('/')[-1].split('.')[0]
                nfo.write_text(NFO_TEMPLATE % dict(title=name, ttid=ttid))
            except Exception as e:
                pb.write(f'failed to process {channel} - {e}')
                errors += 1


if __name__ == '__main__':
    main()
