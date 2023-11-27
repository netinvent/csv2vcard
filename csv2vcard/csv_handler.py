#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard


import os
import pathlib
import csv
from logging import getLogger
import re
from csv2vcard.export_vcard import check_export_dir, export_vcard
from csv2vcard.create_vcard import create_vcard

try:
    from charset_normalizer import detect

    _NORMALIZER = True
except ImportError:
    print(
        "We cannot automagically determine source file encoding. Please install charset_normalizer via pip"
    )
    _NORMALIZER = False


logger = getLogger()


def parse_csv(csv_filename: str, csv_delimiter: str, encoding: str = None) -> dict:
    """
    Simple csv parser with a ; delimiter
    """

    if not encoding and _NORMALIZER:
        with open(csv_filename, "rb") as fp:
            # Read first MB of data
            encoding = detect(fp.read(1024**3))["encoding"]
        logger.info(f"Guessed file encoding: {encoding}")
    else:
        encoding = "utf-8"

    logger.info("Parsing csv..")
    try:
        with open(f"{csv_filename}", "r", encoding=encoding) as fh:
            contacts = csv.reader(fh, delimiter=csv_delimiter)
            header = next(contacts)  # saves header

            # Clean possible ugly CSV files where some jack*ss inserted \r\n or so between fields
            parsed_contacts = []
            pattern = re.compile(r'\n|\t|\r')
            for row in contacts:
                row = [pattern.sub('', sub) for sub in row]
                parsed_contacts.append(dict(zip(header, row)))
            #parsed_contacts = [dict(zip(header, row)) for row in contacts]
            return parsed_contacts
    except OSError as exc:
        logger.error(f"OS error for {csv_filename}: {exc}")
        return []
    except UnicodeDecodeError as exc:
        logger.error(
            f"Failed to decode file with encoding {encoding}. Try to adjust manually with --encoding parameter"
        )
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
    for contact in parse_csv(csv_filename, csv_delimiter, encoding):
        vcard, filename = create_vcard(contact, vcard_version, mapping_file)
        if vcard:
            if not single_vcard_file:
                export_vcard(vcard, output_dir, filename, strip_accents)
            else:
                vcards += "\n" + vcard
                if max_vcard_file_size and len(vcards) > max_vcard_file_size:
                    logger.info(f"Creating sub file for {csv_filename}")
                    export_vcard(
                        vcards,
                        output_dir,
                        os.path.basename(csv_filename) + f"{file_num}.vcf",
                        strip_accents,
                    )
                    file_num = str(int(file_num) + 1)
                    vcards = ""
    if single_vcard_file:
        export_vcard(
            vcards,
            output_dir,
            os.path.basename(csv_filename) + f"{file_num}.vcf",
            strip_accents,
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
