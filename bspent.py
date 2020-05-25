#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import struct


DIRECTORY_ENTRIES_FORMAT = 'll' * 15


def get_directory_entries(bsp_data):
    return list(struct.unpack_from('<' + DIRECTORY_ENTRIES_FORMAT, bsp_data, 4))


def extract(input_bsp_path, output_ent_path):
    with open(input_bsp_path, 'rb') as input_bsp_file:
        input_bsp_data = input_bsp_file.read()

    directory_entries = get_directory_entries(input_bsp_data)
    entity_list_start = directory_entries[0]
    entity_list_end = entity_list_start + directory_entries[1]

    with open(output_ent_path, 'wb') as output_ent_file:
        output_ent_data = input_bsp_data[entity_list_start:entity_list_end]
        output_ent_file.write(output_ent_data)


def switch(input_bsp_path, input_ent_path, output_bsp_path):
    with open(input_bsp_path, 'rb') as input_bsp_file:
        input_bsp_data = input_bsp_file.read()

    with open(input_ent_path, 'rb') as input_ent_file:
        input_ent_data = input_ent_file.read()

    directory_entries = get_directory_entries(input_bsp_data)
    entity_list_start = directory_entries[0]
    entity_list_size = len(input_ent_data)
    entity_list_end = entity_list_start + entity_list_size
    entity_list_size_diff = entity_list_size - directory_entries[1]

    directory_entries[1] = entity_list_size
    for i in range(0, len(directory_entries), 2):
        if directory_entries[i] > entity_list_start:
            directory_entries[i] += entity_list_size_diff

    output_bsp_data = input_bsp_data

    head = output_bsp_data[:4]
    body = struct.pack('<' + DIRECTORY_ENTRIES_FORMAT, *directory_entries)
    tail = output_bsp_data[4 + len(DIRECTORY_ENTRIES_FORMAT) * 4:]
    output_bsp_data = head + body + tail

    head = output_bsp_data[:entity_list_start]
    body = input_ent_data
    tail = output_bsp_data[entity_list_end - entity_list_size_diff:]
    output_bsp_data = head + body + tail

    with open(output_bsp_path, 'wb') as output_bsp_file:
        output_bsp_file.write(output_bsp_data)


def cli():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='command')

    argparser_extract = subparsers.add_parser('extract')
    argparser_extract.add_argument('input_bsp', type=str)
    argparser_extract.add_argument('output_ent', type=str)

    argparser_switch = subparsers.add_parser('switch')
    argparser_switch.add_argument('input_bsp', type=str)
    argparser_switch.add_argument('input_ent', type=str)
    argparser_switch.add_argument('output_bsp', type=str)

    args = argparser.parse_args()

    if args.command == 'extract':
        extract(args.input_bsp, args.output_ent)

    elif args.command == 'switch':
        switch(args.input_bsp, args.input_ent, args.output_bsp)


if __name__ == '__main__':
    cli()
