# -*- coding: utf-8 -*-
import oss2
from oss2.models import PartInfo
from oss2 import determine_part_size
from main import get_bucket
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description='Copy Obj OSS')
    parser.add_argument('-s', '--source')
    parser.add_argument('-d', '--destination')
    return parser, parser.parse_args()


def copy_obj(src_object, dst_object):
    bucket = get_bucket()

    total_size = bucket.head_object(src_object).content_length
    part_size = determine_part_size(total_size, preferred_size=100 * 1024)

    # 初始化分片。
    upload_id = bucket.init_multipart_upload(dst_object).upload_id
    parts = []

    # 逐个分片拷贝。
    part_number = 1
    offset = 0
    while offset < total_size:
        num_to_upload = min(part_size, total_size - offset)
        byte_range = (offset, offset + num_to_upload - 1)

        result = bucket.upload_part_copy(
            bucket.bucket_name, src_object, byte_range, dst_object, upload_id, part_number)
        parts.append(PartInfo(part_number, result.etag))

        offset += num_to_upload
        part_number += 1

    # 完成分片拷贝。
    bucket.complete_multipart_upload(dst_object, upload_id, parts)


def main():
    parser, arguments = parse_arguments()
    if arguments.source and arguments.destination:
        src_object = arguments.source
        dst_object = arguments.destination
        copy_obj(src_object, dst_object)
    else:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
