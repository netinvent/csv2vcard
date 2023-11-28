#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard


import os
import pathlib
import csv
from logging import getLogger
import re
import unicodedata
from csv2vcard.export_vcard import check_export_dir, export_vcard
from csv2vcard.create_vcard import create_vcard
from ofunctions.string_handling import convert_accents
try:
    from charset_normalizer import detect

    _NORMALIZER = True
except ImportError:
    print(
        "We cannot automagically determine source file encoding. Please install charset_normalizer via pip"
    )
    _NORMALIZER = False


logger = getLogger()


def parse_csv(csv_filename: str, csv_delimiter: str, encoding: str = None, strip_accents: bool = True) -> dict:
    """
    Simple csv parser with a ; delimiter
    """

    if not encoding and _NORMALIZER:
        with open(csv_filename, "rb") as fp:
            # Read first MB of data
            encoding = detect(fp.read(1024**3))["encoding"]
        logger.info(f"Guessed file encoding: {encoding}")
    elif not encoding:
        encoding = "utf-8"

    logger.info("Parsing csv..")
    try:
        with open(f"{csv_filename}", "r", encoding=encoding) as fh:
            contacts = csv.reader(fh, delimiter=csv_delimiter)
            header = next(contacts)
            if strip_accents:
                header_parsed = []
                for col in header:
                    header_parsed.append(convert_accents(col))

            # Clean possible ugly CSV files where some jack*ss inserted \r\n or so between fields
            # Also opt in to remove accents when file encoding is unclear
            parsed_contacts = []
            pattern = re.compile(r"\n|\t|\r")
            for row in contacts:
                row_parsed = []
                for col in row:
                    col_parsed = pattern.sub("", col)
                    if strip_accents:
                        col_parsed = convert_accents(col_parsed)
                    row_parsed.append(col_parsed)
                parsed_contacts.append(dict(zip(header_parsed, row_parsed)))
            # parsed_contacts = [dict(zip(header, row)) for row in contacts]
            return parsed_contacts
    except OSError as exc:
        logger.error(f"OS error for {csv_filename}: {exc}")
        return []
    except UnicodeDecodeError as exc:
        logger.error(
            f"Failed to decode file with encoding {encoding}. Try to adjust manually with --encoding parameter. Good test values are 'ansi', 'cp850', 'cp1250', 'unicode_escape'... See Python encodings for more."
        )
        logger.error(f"Error: {exc}")
        return []


def csv2vcard(
    csv_filename: str,
    csv_delimiter: str = ";",
    mapping_file: str = None,
    encoding: str = None,
    output_dir: str = None,
    vcard_version: int = 4,
    single_vcard_file: bool = False,
    max_vcard_file_size: int = None,
    max_vcards_per_file: int = None,
    strip_accents: bool = False,
) -> None:
    """
    Main function
    """
    check_export_dir(output_dir)

    vcards = ""
    if max_vcard_file_size:
        # Make sure we are counting in KB
        max_vcard_file_size *= 1024
        file_num = "1"
    else:
        max_vcard_file_size = None
        file_num = ""
    if max_vcards_per_file:
        file_num = 1
    else:
        file_num = ""
    count = 0
    for contact in parse_csv(csv_filename, csv_delimiter, encoding, strip_accents):
        vcard, filename = create_vcard(contact, vcard_version, mapping_file)
        if vcard:
            count += 1
            if not single_vcard_file:
                export_vcard(vcard, output_dir, filename)
            else:
                vcards += "\n" + vcard
                if (max_vcard_file_size and len(vcards) > max_vcard_file_size) \
                or (max_vcards_per_file and count >= max_vcards_per_file):
                    logger.info(f"Creating sub file for {csv_filename}")
                    export_vcard(
                        vcards,
                        output_dir,
                        os.path.basename(csv_filename) + f"{file_num}.vcf",
                    )
                    file_num = str(int(file_num) + 1)
                    vcards = ""
                    count = 0
    if single_vcard_file:
        export_vcard(
            vcards,
            output_dir,
            os.path.basename(csv_filename) + f"{file_num}.vcf",
        )


def interface_entrypoint(config: dict) -> bool:
    settings = config["settings"]
    source = pathlib.Path(settings["csv_filename"])
    sources = []
    if not os.path.exists(source):
        logger.error(f"Source path does not exist")
        return False
    elif os.path.isdir(source):
        sources = source.glob("**/*.csv")
    else:
        sources = [source]

    if len(settings["csv_delimiter"]) != 1:
        logger.error(f"CSV Delimiter char should be exactly one character")
        return False

    max_vcard_file_size = settings["max_vcard_file_size"]
    if max_vcard_file_size:
        try:
            settings["max_vcard_file_size"] = int(max_vcard_file_size)
        except TypeError:
            logger.error(f"Max vcard file size should be an integer")
            return False

    for src in sources:
        settings["csv_filename"] = src
        logger.info(f"Running conversion for {src}")
        csv2vcard(**settings)
    return True
