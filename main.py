import os
import sys
import argparse
import pathlib
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
from oss2.headers import OSS_OBJECT_TAGGING
import oss2
import urllib
import requests

from Configs import ACCESS_KEY_ID, ACCESS_KEY_SECRET, OSS_ENDPOINT, BUCKET_NAME, URL_SHORTENER_API_KEY


def parse_arguments():
    parser = argparse.ArgumentParser(description='Upload OSS')
    parser.add_argument('-f', '--file')
    parser.add_argument('-d', '--oss-dir')
    return parser, parser.parse_args()


def get_bucket():
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, BUCKET_NAME)
    return bucket


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print(f"Consumed MB: {int(consumed_bytes / 1000 / 1000)}")
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


def upload(key, filepath, filename):
    bucket = get_bucket()

    # headers = dict()
    # headers[OSS_OBJECT_TAGGING] = f"type={objtype}"

    total_size = os.path.getsize(filepath)
    part_size = determine_part_size(total_size, preferred_size=1000000 * 1024)

    upload_id = bucket.init_multipart_upload(key).upload_id
    parts = []

    with open(filepath, 'rb') as fileobj:
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(key, upload_id, part_number,
                                        SizedFileAdapter(fileobj, num_to_upload), progress_callback=percentage)
            parts.append(PartInfo(part_number, result.etag))

            offset += num_to_upload
            part_number += 1

    bucket.complete_multipart_upload(key, upload_id, parts)

    # gen_signed_url(bucket, key, filename)


def gen_signed_url(bucket, objname, filepath=''):
    signed_url = bucket.sign_url('GET', objname, 32400)
    short_url = gen_short_url(signed_url)
    print(f"\n\n{objname}\n{short_url}\n{signed_url}")

    sign_url_dir = os.path.join(
        str(pathlib.Path(__file__).resolve().parent), 'signed_url')
    if not os.path.exists(sign_url_dir):
        os.mkdir(sign_url_dir)
    txt_path = filepath if filepath else sign_url_dir + \
        '/' + objname.replace('/', '-')
    text = objname + '\n' + short_url + '\n' + signed_url
    with open(txt_path, "w") as text_file:
        print(text, file=text_file)
    return (objname, short_url, signed_url)


def gen_short_url(url):
    url = urllib.parse.quote(url)
    url_shortener_api_url = f'https://cutt.ly/api/api.php?key={URL_SHORTENER_API_KEY}&short={url}'
    r = requests.get(url_shortener_api_url)
    json = r.json()
    short_url = json['url']['shortLink']
    return short_url


def main():
    parser, arguments = parse_arguments()
    filepath = arguments.file
    if filepath:
        key = []
        filename = os.path.basename(filepath)
        if arguments.oss_dir:
            key = arguments.oss_dir + '/' + filename
        else:
            key = filename
        upload(key, filepath, filename)
    else:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
