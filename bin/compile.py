#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard

__intname__ = "NetInvent Python Tools Compiler Script"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2023 NetInvent"
__license__ = "GPL-3.0-only"
__build__ = "2023112501"
__version__ = "2.0.0"


"""
Nuitka compilation script tested for
 - windows 32 bits (Vista+)
 - windows 64 bits
 - Linux i386
 - Linux i686
 - Linux armv71
"""


import sys
import os
import argparse
import atexit
from command_runner import command_runner
from ofunctions.platform import python_arch, get_os


# Insert parent dir as path se we get to use our package
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))


from csv2vcard.customization import (
    COMPANY_NAME,
    TRADEMARKS,
    PRODUCT_NAME,
    FILE_DESCRIPTION,
    COPYRIGHT,
    # LICENSE_FILE,
)
from csv2vcard.path_helper import BASEDIR
import glob


del sys.path[0]


def _read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def get_metadata(package_file):
    """
    Read metadata from package file
    """

    _metadata = {}

    for line in _read_file(package_file).splitlines():
        if line.startswith("__version__") or line.startswith("__description__"):
            delim = "="
            _metadata[line.split(delim)[0].strip().strip("__")] = (
                line.split(delim)[1].strip().strip("'\"")
            )
    return _metadata


def have_nuitka_commercial():
    try:
        import nuitka.plugins.commercial

        print("Running with nuitka commercial")
        return True
    except ImportError:
        print("Running with nuitka open source")
        return False


def compile(arch: str, target: str, has_gui: bool = False):
    if os.name == "nt":
        program_executable = target + ".exe"
        platform = "windows"
    elif sys.platform.lower() == "darwin":
        platform = "darwin"
        program_executable = target
    else:
        platform = "linux"
        program_executable = target

    BUILDS_DIR = os.path.abspath(os.path.join(BASEDIR, os.pardir, "BUILDS"))
    OUTPUT_DIR = os.path.join(BUILDS_DIR, platform, arch)

    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    PYTHON_EXECUTABLE = sys.executable

    # npbackup compilation
    # Strip possible version suffixes '-dev'
    _program_version = program_version.split("-")[0]
    PRODUCT_VERSION = _program_version + ".0"
    FILE_VERSION = _program_version + ".0"

    file_description = f"{FILE_DESCRIPTION} P{sys.version_info[1]}"

    # translations_dir = "translations"
    # translations_dir_source = os.path.join(BASEDIR, translations_dir)
    # translations_dir_dest = os.path.join(PACKAGE_DIR, translations_dir)

    # license_dest_file = os.path.join(PACKAGE_DIR, os.path.basename(LICENSE_FILE))

    icon_file = os.path.join(PACKAGE_DIR, "netperfect.ico")

    NUITKA_OPTIONS = ""
    NUITKA_OPTIONS += " --enable-plugin=data-hiding" if have_nuitka_commercial() else ""

    # Stupid fix for synology RS816 where /tmp is mounted with `noexec`.
    if "arm" in arch:
        NUITKA_OPTIONS += " --onefile-tempdir-spec=/var/tmp"

    if has_gui:
        NUITKA_OPTIONS += " --disable-console --plugin-enable=tk-inter"
    else:
        NUITKA_OPTIONS += f" --enable-console --plugin-disable=tk-inter --nofollow-import-to=PySimpleGUI --nofollow-import-to=_tkinter --nofollow-import-to={PACKAGE_NAME}.gui"

    if os.name != "nt":
        NUITKA_OPTIONS += f" --nofollow-import-to={PACKAGE_NAME}.windows"

    EXE_OPTIONS = f'--company-name="{COMPANY_NAME}" --product-name="{PRODUCT_NAME}" --file-version="{FILE_VERSION}" --product-version="{PRODUCT_VERSION}" --copyright="{COPYRIGHT}" --file-description="{file_description}" --trademarks="{TRADEMARKS}"'
    # CMD = f'{PYTHON_EXECUTABLE} -m nuitka --python-flag=no_docstrings --python-flag=-O {NUITKA_OPTIONS} {EXE_OPTIONS} --onefile --include-data-dir="{translations_dir_source}"="{translations_dir_dest}" --include-data-file="{LICENSE_FILE}"="{license_dest_file}" --include-data-file="{restic_source_file}"="{restic_dest_file}" --windows-icon-from-ico="{icon_file}" --output-dir="{OUTPUT_DIR}" bin/{target}'
    CMD = f'{PYTHON_EXECUTABLE} -m nuitka --python-flag=no_docstrings --python-flag=-O {NUITKA_OPTIONS} {EXE_OPTIONS} --onefile --windows-icon-from-ico="{icon_file}" --output-dir="{OUTPUT_DIR}" bin/{target}'

    print(CMD)
    errors = False
    exit_code, output = command_runner(CMD, timeout=0, live_output=True)
    if exit_code != 0:
        errors = True

    print("COMPILE ERRORS", errors)
    return not errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="netinvent compile.py",
        description="Compiler script for NetInvent Python projetcs",
    )

    program_version = get_metadata(os.path.join(BASEDIR, "__main__.py"))["version"]

    PACKAGE_NAME = "csv2vcard"
    PACKAGE_DIR = "csv2vcard"
    TARGETS = ["csv2vcard-cli", "csv2vcard-gui"]

    errors = False
    for target in TARGETS:
        try:
            if target.endswith("-gui"):
                has_gui = True
            else:
                has_gui = False
            result = compile(arch=python_arch(), target=target, has_gui=has_gui)
            if not result:
                print("ERRORS IN BUILD PROCESS")
                errors = True
            else:
                print("SUCCESS BUILDING")
        except Exception:
            print("COMPILATION FAILED")
            raise
