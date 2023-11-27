#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard

__intname__ = "sign_windows_executables"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2023 NetInvent"
__license__ = "GPL-3.0-only"
__build__ = "2023112601"
__version__ = "1.1.0"


import os
import sys
from ofunctions.file_utils import get_paths_recursive
try:
    from windows_tools.signtool import SignTool
except ImportError as exc:
    print(f"This tool needs windows_tools.signtool >= 0.4.0: {exc}")
    sys.exit(1)
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from csv2vcard.path_helper import BASEDIR

del sys.path[0]

if __name__ == "__main__":
    PACKAGE_DIR = "csv2vcard"
    BINARIES = ["csv2vcard-cli.exe", "csv2vcard-gui.exe"]

    EXECUTABLES_DIR = os.path.join(BASEDIR, os.pardir, "BUILDS")

    signer = SignTool()

    files = get_paths_recursive(EXECUTABLES_DIR, f_include_list=BINARIES, exclude_dirs=True)
    for file in files:
        print(f"Signing {file}")
        result = signer.sign(file, bitness=64)
        if not result:
            raise EnvironmentError(
            "Could not sign executable ! Is the PKI key connected ?"
        )
