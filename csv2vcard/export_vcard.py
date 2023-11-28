#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard


import os
from logging import getLogger


logger = getLogger()


def export_vcard(vcard: str, output_dir: str, filename: str):
    """
    Exporting a vCard in one or multiple files
    """
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(vcard)
            fp.close()
            logger.info(f"Created vCard for {filename}")
    except OSError as exc:
        logger.critical(f"Could not write file {filepath}: {exc}")


def check_export_dir(output_dir: str) -> None:
    """
    Checks if export folder exists in directory
    """
    if not os.path.exists(output_dir):
        logger.info(f"Creating {output_dir} folder...")
        os.makedirs(output_dir)
