#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard


import os
import unicodedata


def strip_accents(string):
    """
    From https://stackoverflow.com/a/518232/2635443
    """

    return "".join(
        c
        for c in unicodedata.normalize("NFD", string)
        if unicodedata.category(c) != "Mn"
    )


def export_vcard(vcard: str, output_dir: str, filename: str, normalize: bool = False):
    """
    Exporting a vCard in one or multiple files
    Optional normalization (remove all accents) from names
    """
    filepath = os.path.join(output_dir, filename)
    if normalize:
        vcard = strip_accents(vcard)
    try:
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(vcard)
            fp.close()
            print(f"Created vCard for {filename}")
    except OSError as exc:
        print(f"Could not write file {filepath}: {exc}")


def check_export_dir(output_dir: str) -> None:
    """
    Checks if export folder exists in directory
    """
    if not os.path.exists(output_dir):
        print(f"Creating {output_dir} folder...")
        os.makedirs(output_dir)
