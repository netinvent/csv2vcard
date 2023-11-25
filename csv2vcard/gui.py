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


from typing import Union
import sys
import os
import json
from csv2vcard.csv_handler import interface_entrypoint
from ofunctions.threading import threaded, Future
import ofunctions.logger_utils
from csv2vcard.customization import *

try:
    import PySimpleGUI as sg
except ImportError as exc:
    print(
        "Module not found. If tkinter is missing, you need to install it from your distribution. See README.md file"
    )
    print("Error: {}".format(exc))
    sys.exit(203)

from csv2vcard.path_helper import CURRENT_DIR


LOG_FILE = os.path.join(CURRENT_DIR, "{}.log".format(__intname__))
logger = ofunctions.logger_utils.logger_get_logger(LOG_FILE)


GUI_VARS = [
    "csv_filename",
    "csv_delimiter",
    "encoding",
    "mapping_file",
    "output_dir",
    "vcard_version",
    "single_vcard_file",
    "max_vcard_file_size",
    "strip_accents",
]


def get_config_from_gui(values: dict) -> Union[dict, bool]:
    config = {"software": {"name": __intname__}, "settings": {}}
    for gui_var in GUI_VARS:
        config["settings"][gui_var] = values[f"-{gui_var}-"]

    return config


def update_gui_from_config(window: sg.Window, config: dict) -> bool:
    try:
        if config["software"]["name"] != __intname__:
            raise EnvironmentError
    except Exception:
        sg.PopupError("Invalid configuration file")
        return False
    for gui_var, value in config["settings"].items():
        window[f"-{gui_var}-"].update(value)

    return True


def gui_interface():
    """
    Main GUI
    """

    sg.theme(PYSIMPLEGUI_THEME)
    sg.SetOptions(icon=OEM_ICON)

    main_col = [
        [
            sg.Text("CSV File/Folder", size=(26, 1)),
            sg.In(size=(25, 1), key="-csv_filename-"),
            sg.FileBrowse("Select file", target="-csv_filename-"),
            sg.FolderBrowse("Select folder", target="-csv_filename-"),
        ],
        [
            sg.Text("CSV Delimiter char", size=(26, 1)),
            sg.In(";", size=(2, 1), key="-csv_delimiter-"),
        ],
        [
            sg.Text("Source file encoding", size=(26, 1)),
            sg.In("", size=(25, 1), key="-encoding-"),
        ],
        [
            sg.Text(" ", size=(26, 1)),
            sg.Text(
                "Leave empty for autodetection or use utf-8, or cp1250, unicode..."
            ),
        ],
        [
            sg.Text("Alternative CSV Mapping", size=(26, 1)),
            sg.In(size=(25, 1), key="-mapping_file-"),
            sg.FileBrowse("Select JSON map file"),
        ],
        [
            sg.Text("Destination folder", size=(26, 1)),
            sg.In(size=(25, 1), key="-output_dir-"),
            sg.FolderBrowse("Select folder"),
        ],
        [
            sg.Text("vCard version", size=(26, 1)),
            sg.Combo([3, 4], default_value=4, key="-vcard_version-"),
        ],
        [
            sg.Checkbox(
                "Create a single vCard file from a CSV",
                key="-single_vcard_file-",
                enable_events=True,
            ),
            sg.Text("Max vCard file size (KB)"),
            sg.In(size=(10, 1), key="-max_vcard_file_size-", disabled=True),
        ],
        [sg.Checkbox("Strip accents from vCards", key="-strip_accents-")],
        [
            sg.Text(" " * 26),
            sg.Button("Exit", key="-EXIT-"),
            sg.SaveAs("Export settings", target="-EXPORT_SETTINGS_FILENAME-"),
            sg.Input(
                "", key="-EXPORT_SETTINGS_FILENAME-", enable_events=True, visible=False
            ),
            sg.FileBrowse("Import settings", target="-IMPORT_SETTINGS_FILENAME-"),
            sg.Input(
                "", key="-IMPORT_SETTINGS_FILENAME-", enable_events=True, visible=False
            ),
            sg.Button("Launch conversion", key="-CONVERT-"),
        ],
    ]

    window = sg.Window(f"NetInvent csv2vCard GUI {__version__}", main_col)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break
        if event == "-single_vcard_file-":
            window["-max_vcard_file_size-"].update(
                disabled=not values["-single_vcard_file-"]
            )
        if event == "-EXPORT_SETTINGS_FILENAME-":
            config_filename = values["-EXPORT_SETTINGS_FILENAME-"]
            if config_filename.split(".")[0] != "json":
                config_filename = config_filename.split(".")[0] + ".json"
            config = get_config_from_gui(values)
            try:
                with open(config_filename, "w", encoding="utf-8") as file_handle:
                    json.dump(config, file_handle)
                sg.Popup(f"Configuration written to {config_filename}")
            except OSError as exc:
                sg.PopupError(f"Cannot write file {config_filename}: {exc}")
        if event == "-IMPORT_SETTINGS_FILENAME-":
            config_filename = values["-IMPORT_SETTINGS_FILENAME-"]
            try:
                with open(config_filename, "r", encoding="utf-8") as file_handle:
                    config = json.load(file_handle)
                    update_gui_from_config(window, config)
                    sg.Popup(f"Config imported from {config_filename}")
            except Exception as exc:
                sg.PopupError(f"Could not import config file {config_filename}: {exc}")
        if event == "-CONVERT-":
            config = get_config_from_gui(values)
            result = _interface_entrypoint(config)
            if result:
                sg.Popup("Conversion done")
            else:
                sg.Popup("Conversion failed, please see log file")


@threaded
def __interface_entrypoint(config: dict) -> Future:
    """
    Simple wrapper to make that function a thread
    """
    return interface_entrypoint(config)


def _interface_entrypoint(config: dict) -> bool:
    """
    Simple wrapper to show loader animation
    """
    # We get a thread result, hence pylint will complain the thread isn't a tuple
    # pylint: disable=E1101 (no-member)
    thread = __interface_entrypoint(config)
    while not thread.done() and not thread.cancelled():
        sg.PopupAnimated(
            LOADER_ANIMATION,
            message="Running conversions",
            time_between_frames=50,
            background_color=GUI_LOADER_COLOR,
            text_color=GUI_LOADER_TEXT_COLOR,
        )
    sg.PopupAnimated(None)
    return thread.result()


def main():
    try:
        gui_interface()
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
