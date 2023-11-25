#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard

__intname__ = "csv2vcard"
__author__ = "Nikolay Dimolarov (https://github.com/tech4242), Carlos V (https://github.com/ReallyCoolData) Orsiris de Jong (https://github.com/deajan)"
__site__ = "github.com/netinvent/csv2vcard"
__description__ = "Transform CSV files into vCards"
__copyright__ = "Copyright (C) 2017-2023 Nikolay Dimolarov, Carlos V, Orsiris de Jong"
__license__ = "MIT License"
__build__ = "2023112501"
__version__ = "0.6.0"


import os
import sys
from argparse import ArgumentParser
import ofunctions.logger_utils
from csv2vcard.csv_handler import interface_entrypoint
from csv2vcard.path_helper import CURRENT_DIR


LOG_FILE = os.path.join(CURRENT_DIR, "{}.log".format(__intname__))
logger = ofunctions.logger_utils.logger_get_logger(LOG_FILE)


def cli_interface():
    parser = ArgumentParser(
        prog=__intname__,
        description=f"""{__intname__} {__version__} {__description__} {__copyright__}
This program is distributed under the MIT Public License and comes with ABSOLUTELY NO WARRANTY.\n
This is free software, and you are welcome to redistribute it under certain conditions; See Licence file for more info.""".format(),
    )

    parser.add_argument(
        "-s",
        "--source",
        type=str,
        dest="source",
        default=None,
        required=True,
        help="Path to source CSV file / folder containing CSV files",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output_dir",
        default=None,
        required=True,
        help="Path to destination folder",
    )

    parser.add_argument(
        "--vcard-version",
        type=int,
        dest="vcard_version",
        default=4,
        required=False,
        help="vCard version (3 or 4), defaults to 4",
    )

    parser.add_argument(
        "--single-vcard",
        action="store_true",
        default=False,
        help="Create a single VCF file with multiple entries",
    )

    parser.add_argument(
        "-m",
        "--mapping",
        type=str,
        dest="mapping_file",
        default=None,
        required=False,
        help="Path to optional data mapping",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        dest="delimiter",
        default=";",
        required=False,
        help="CSV delimiter character",
    )

    parser.add_argument(
        "--encoding",
        type=str,
        dest="encoding",
        default=None,
        required=False,
        help="Optional encoding for CSV file",
    )

    parser.add_argument(
        "--max-vcard-file-size",
        type=int,
        dest="max_vcard_file_size",
        default=None,
        required=False,
        help="Optional size limit for single vCard files",
    )

    parser.add_argument(
        "--strip-accents",
        action="store_true",
        default=False,
        help="Optional strip accents from vCards for max compatibility",
    )

    args = parser.parse_args()
    version_string = f"{__intname__} {__version__}\n{__description__}\n{__copyright__}"
    print(version_string)

    config = {}
    config["csv_filename"] = args.source
    config["csv_delimiter"] = args.delimiter
    config["mapping_file"] = args.mapping_file
    config["encoding"] = args.encoding
    config["output_dir"] = args.output_dir
    config["vcard_version"] = args.vcard_version
    config["single_vcard_file"] = args.single_vcard
    config["max_vcard_file_size"] = args.max_vcard_file_size
    config["strip_accents"] = args.strip_accents
    interface_entrypoint(config)


def main():
    try:
        cli_interface()
    except KeyboardInterrupt as exc:
        logger.critical(f"Program interrupted by keyboard. {exc}")
        # EXIT_CODE 200 = keyboard interrupt
        sys.exit(200)
    except Exception as exc:
        logger.critical(f"Program interrupted by error. {exc}")
        logger.critical("Trace:", exc_info=True)
        # EXIT_CODE 201 = Non handled exception
        sys.exit(201)


if __name__ == "__main__":
    main()
