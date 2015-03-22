__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

# only for five letter images at the moment

import requests
import re
import shutil
import os


def get_img_links(url):
    req = requests.get(url)

    if req.status_code != 200:
        return []

    return clean_up(re.findall(r'data-src="//(.*?)"', req.text))


def clean_up(coarse_urls):
    clean_urls = []

    for url in coarse_urls:
        # if url[1][-1] != '4':  # mp4 exclusion
        #     if url[1][-4:] == 'webm':  # webm to gif conversion
        #         clean_urls += ['http:' + url[1][:-4] + 'gif']
        #     else:

        clean_urls += ['http://' + url[:17] + url[18:]]

    return clean_urls  # because reasons


def download_imgs(album_url, folders=False):
    imgs = get_img_links(album_url)

    if folders:  # doesn't really work yet
        os.makedirs('out/jpgs', exist_ok=True)
        os.makedirs('out/pngs', exist_ok=True)
        os.makedirs('out/webms', exist_ok=True)
        os.makedirs('out/others', exist_ok=True)
    else:
        os.makedirs('downloaded', exist_ok=True)

    for img in imgs:
        response = requests.get(img, stream=True)

        filename = re.findall(r'm/.*', img)[0][2:]  # lol I know
        extension = re.findall(r'\..*', filename)[0][1:]

        if folders:
            path = 'out/' + extension + 's' + filename
        else:
            path = 'downloaded/' + filename

        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


if __name__ == '__main__':
    with open('imgur_links.txt', 'r') as links:
        albums = links.read().splitlines()

    for album in albums:
        if album[0] != "#":
            download_imgs(album)