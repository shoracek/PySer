#!/usr/bin/env python3

import pretty_printer
from common import parsed_fields_long, parsed_fields_short
import title_parser
import versions_parser
import table_of_contents_parser
import revisions_parser
import bibliography_parser
import argparse
import itertools
import json
import os
import sys
from typing import List


def parse(plain_text: str):
    """
    Parse the plaintext contents of a single document into
    a JSON-corresponding dictionary.
    """

    return {
        "title": title_parser.parse(plain_text),
        "versions": versions_parser.parse(plain_text),
        "table_of_contents": table_of_contents_parser.parse(plain_text),
        "revisions": revisions_parser.parse(plain_text),
        "bibliography": bibliography_parser.parse(plain_text),
        "other": [],
    }


def generate_json_file(sequence_number: int, input_path: str,
                       output_path: str, pretty_printed_fields: List[str]):
    """
    Perform parsing of a single document and serialization of the resultant
    JSON, with optional pretty-printing.
    """

    max_read = 64 * 1024 * 1024

    with open(input_path, "r", encoding="utf8") as file:
        plain_text = file.read(max_read)
        if len(plain_text) == max_read:
            raise MemoryError("File is too large")

    result = parse(plain_text)
    output = json.dumps(result, indent=4, ensure_ascii=False)

    if len(pretty_printed_fields) != 0:
        if sequence_number != 1:
            print(end="\n" * 2)
        print(f"{sequence_number}.",
              os.path.splitext(os.path.basename(input_path))[0])

    pretty_printer.pretty_print(result, pretty_printed_fields)

    with open(output_path, "w", encoding="utf8") as file:
        file.write(output)


def generate_multiple_json_files(input_files: List[str], output_folder: str,
                                 pretty_printed_fields: List[str]):
    """
    Perform parsing and results serialization of multiple documents,
    sequentially.
    """

    if not os.path.isdir(output_folder):
        print(f"No such directory: '{output_folder}'", file=sys.stderr)
        return

    for i, input_file in enumerate(input_files, start=1):
        basename = os.path.splitext(input_file)[0]
        basename = os.path.basename(basename)
        output_file = os.path.join(output_folder, basename + ".json")

        try:
            generate_json_file(i, input_file, output_file,
                               pretty_printed_fields)
        except Exception as e:
            print(f"Skipping file '{input_file}': {e}", file=sys.stderr)


def parsed_fields(string: str) -> List[str]:
    """
    Parse the comma-separated list of fields, taking only the first occurence
    of each option.
    """

    if len(string) == 0:
        return []

    fields = string.split(",")
    fields = list(itertools.chain.from_iterable(
        parsed_fields_long if f == "all" else [f] for f in fields))

    for i in range(len(fields)):
        try:
            fields[i] = \
                parsed_fields_long[parsed_fields_short.index(fields[i])]
        except ValueError:
            pass

    if any(field not in parsed_fields_long for field in fields):
        raise argparse.ArgumentTypeError(
            f"'{string}' is not a valid fields option")

    fields = list(dict.fromkeys(fields))
    return fields


def parse_args():
    """Parse the command-line arguments."""

    argument_parser = argparse.ArgumentParser(
        description="PySer - A regular expression based parser for security "
                    "certificates.")

    argument_parser.add_argument(
        "input_files",
        help="A list of input files in plaintext format.",
        type=str, nargs='+')
    argument_parser.add_argument(
        "-o", "--output_folder",
        help="Path to an existing outupt folder, into which "
             "the correspondingly named list of JSON files will be written.",
        type=str, default=".")
    argument_parser.add_argument(
        "-p", "--pretty_print",
        help="A comma-separated list of the fields (without whitespace) "
             "to pretty-print after parsing each file. Allowed values are: " +
             ", ".join(parsed_fields_long) +
             " or their corresponding short form: " +
             ", ".join(parsed_fields_short) +
             ". The fields are printed in the specified order, "
             "without duplication.",
        metavar="FIELD_LIST",
        type=parsed_fields, default="")
    return argument_parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_multiple_json_files(args.input_files,
                                 args.output_folder,
                                 args.pretty_print)
