#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard


from typing import Tuple
import base64
from binascii import Error as binascii_Error
from datetime import datetime
import json


# Vcard mappings
# BEGIN:VCARD
# VERSION:2.1|3.0|4.0
# ADR,TYPE=HOME|WORK:Postbox;Adress with street number;City;Region;ZIP;Country
# ANNIVERSARY:YYYYMMJJ|ISO8601-date
# BDAY:YYYYMMJJ|ISO8601-date
# CATEGORGIES:[comma separated tags]
# EMAIL:[emailadr]
# FN:[Formatted Name]                                                       << Optional in v2, required in v3 and v4
# GENDER:'':M|F|O|N|U                                                       # Only exists in v4
# GEO:lat;long                                                              # V3 syntax
# GEO;geo:lat;long                                                          # V4 syntax
# KEY;TYPE=PGP:http://example.tld/key.gpg                                   # V3 URI syntax
# KEY;TYPE=PGP;ENCODING=B:[base64-data]                                     # V3 inline syntax
# KEY;MEDIATYPE=application/pgp-keys:https://example.tld.key.pgp            # V4 URI instax
# KEY:data:application/pgp-keys;base64,[base64-data]                        # V4 inline syntax
# LOGO;TYPE=PNG:http://example.tld/logo.png                                 # V3 URI syntax
# LOGO;TYPE=PNG;ENCODING=B:[base64-data]                                    # V3 inline syntax
# LOGO;MEDIATYPE=image/png:http://example.tld/logo.png                      # V4 URI syntax
# LOGO:data:image/png;base64,[base64-data]                                  # V4 inline syntax
# N:LastName;FirstName;SecondName;Title;Suffix                              << Required in v2 and v3, optional in v4
# NOTE:[text]
# NICKNAME:[comma separated text]
# ORG:[comma separated texts, from most global left to most precise right]
# PHOTO;TYPE=JPEG:http://example.tld/photo.jpg                              # V3 URI syntax
# PHOTO;TYPE=JPEG;ENCODING=B:[base64-data]                                  # V3 inline syntax
# PHOTO;MEDIATYPE=image/jpeg:http://example.tld/photo.jpg                   # V4 URI syntax
# PHOTO:data:image/jpeg;base64,[base64-data]                                # V4 inline syntax
# REV:[ISO8601-date timestamp for last vcard revision]
# ROLE:[text]
# SOURCE:http://example.tld/me.vcf
# TEL;TYPE=HOME|WORK,CELL|FAX|PAGER,VOICE,VIDEO,TEXT,TEXTPHONE:[phone number]
# TITLE:[text]
# TZ:+0100                                                                  # V3 syntax
# TZ:Europe/Paris                                                           # V4 syntax
# UID:urn:uuid:abcdefgh-0123-4567-8901-abcdefghijkl
# URL:http://example.tld
# END:VCARD


# This is the default mapping, where each lowercase value is a column in the source CSV file
default_mapping = {
    "ADR": {
        "TYPE": {
            "HOME": ["postbox_home", "address_home", "city_home", "region_home", "zip_home", "country_home"],
            "WORK": ["postbox", "address", "city", "region", "zip", "country"],
        }
    },
    "ANNIVERSARY": "anniversary",
    "BDAY": "birthday",
    "CATEGORIES": "categories",
    "EMAIL": {"TYPE": {"HOME": "email_home", "WORK": "email"}},
    "FN": {
        "CONCAT": ["title", "last_name", "first_name"],
    },
    "GENDER": "gender",
    "GEO": "geo",
    "KEY": "key",
    "LOGO": "logo",
    "N": ["last_name", "first_name", "second_name", "title", "suffix"],
    "NOTE": "remarks",
    "NICKNAME": "nickname",
    "ORG": "company",
    "PHOTO": "photo",
    "ROLE": "role",
    "TEL": {
        "TYPE": {
            "HOME,CELL": "mobile_phone_home",
            "HOME,FAX": "fax_home",
            "HOME,PAGER": "pager_home",
            "HOME,VOICE": "phone_home",
            "HOME,VIDEO": "video_phone_home",
            "HOME,TEXTPHONE": "text_phone_home",
            "HOME,TEXT": "text_home",
            "WORK,CELL": "mobile_phone",
            "WORK,FAX": "fax",
            "WORK,PAGER": "pager",
            "WORK,VOICE": "phone",
            "WORK,VIDEO": "video_phone",
            "WORK,TEXTPHONE": "text_phone",
            "WORK,TEXT": "text",
        }
    },
    "TITLE": "title",
    "TZ": "timezone",
    "UID": "uuid",
    "URL": "webpage",
}


def load_mapping_file(mapping_file: str):
    """
    Loads a JSON mapping file
    """

    with open(mapping_file, "r", encoding="utf-8") as fp:
        return json.load(fp)


def create_vcard(
    contact: dict, version: int = 4, mapping_file: dict = None
) -> Tuple[str, str]:
    """
    The mappings used below are from https://www.w3.org/TR/vcard-rdf/#Mapping
    """

    if version not in [3, 4]:
        raise ValueError("Incorrect Vcard version given. Currently supported: 3 or 4.")
    if not mapping_file:
        mapping = default_mapping
    else:
        mapping = load_mapping_file(mapping_file)

    vcard_map = {}
    for key, value in mapping.items():
        # Don't bother when no mapping is available
        if not value:
            continue

        # Handle all keys with TYPE
        try:
            mapping[key]["TYPE"]
        except (KeyError, TypeError):
            pass
        else:
            for type_key, type_value in mapping[key]["TYPE"].items():
                idkey = f"{key}-{type_key}-{type_value}"
                if isinstance(mapping[key]["TYPE"][type_key], list):
                    vcard_map[idkey] = f"{key};TYPE={type_key}:"
                    mapping_len = len(mapping[key]["TYPE"][type_key])
                    for num, sub_key in enumerate(mapping[key]["TYPE"][type_key]):
                        if sub_key:
                            try: 
                                if num == mapping_len - 1:
                                    vcard_map[idkey] += f"{contact[sub_key]}"
                                else:
                                    vcard_map[idkey] += f"{contact[sub_key]};"
                            except KeyError:
                                if num < mapping_len - 1:
                                    vcard_map[idkey] += ";"
                                print(f"1010: CSV file has no key {sub_key}")

                else:
                    # Emails are handled here
                    try:
                        if (
                            mapping[key]["TYPE"][type_key]
                            and contact[mapping[key]["TYPE"][type_key]]
                        ):
                            if key == "EMAIL" and not '@' in contact[mapping[key]["TYPE"][type_key]]:
                                print(f"1014: No valid email addres in {contact}")
                                continue
                            vcard_map[
                                id
                            ] = f"{key};TYPE={type_key}:{contact[mapping[key]['TYPE'][type_key]]}"
                    except (KeyError, TypeError):
                        print(f"1001: CSV file has no key {type_value}")

            continue

        # Handle special concatenation case for FN where multiple colunms will be concatenated to a string
        # Also removes unecessary separator characters
        try:
            mapping[key]["CONCAT"]
        except TypeError:
            pass
        else:
            if isinstance(mapping[key]["CONCAT"], list):
                fn_entry = ""
                for sub_key in mapping[key]["CONCAT"]:
                    if sub_key:
                        try:
                            data = contact[sub_key]
                            for char in [",", ";", ":"]:
                                # TODO: We could check if left or right has a space, and depending on it, replace with ' ' or ''
                                data = data.replace(char, "")
                            fn_entry += data.strip()
                        except KeyError:
                            print(f"1011: CSV file has no key {sub_key}")
                if not fn_entry.strip():
                    print(f"1012: No Valid FN entry for {contact}")
                else:
                    vcard_map[key] = f"{key}:{fn_entry.strip()}"
                continue
            else:
                print(f"1013: Key {key} with CONCAT does not contain a list of columns to concatenate")
                continue

        # Handle all list types
        if isinstance(mapping[key], list):
            vcard_map[key] = f"{key}:"
            for num, sub_key in enumerate(mapping[key]):
                if sub_key:
                    try:
                        if num == mapping_len - 1:
                            vcard_map[key] += f"{contact[sub_key]}"
                        else:
                            vcard_map[key] += f"{contact[sub_key]};"
                    except KeyError:
                        if num < mapping_len - 1:
                            vcard_map[key] += ";"
                        print(f"1002: CSV file has no key {sub_key}")
            continue

        # Handle special cases for KEY, LOGO and PHOTO
        if key in ["KEY", "LOGO", "PHOTO"]:
            try:
                contact_value = contact[value].strip()
            except KeyError:
                print(f"1003: CSV file has no key {value}")
                continue

            if key == "KEY":
                data_type = {3: "PGP", 4: "application/pgp-keys"}
            if key == "LOGO":
                data_type = {3: "PNG", 4: "application/png"}
            if key == "PHOTO":
                data_type = {3: "JPEG", 4: "image/jpeg"}

            if contact_value.lower().startswith("http"):
                if version == 3:
                    vcard_map[key] = f"{key};TYPE={data_type[3]}:{contact[value]}"
                if version == 4:
                    vcard_map[key] = f"{key};MEDIATYPE={data_type[4]}:{contact[value]}"
            else:
                try:
                    base64.b64decode(contact[value])
                except (TypeError, binascii_Error):
                    print(
                        f"1005: Contact key {key} has bogus data (no URI nor B64 encoded data)"
                    )
                    continue

                if version == 3:
                    vcard_map[
                        key
                    ] = f"{key};TYPE={data_type[3]};ENCODING=b:{contact[value]}"
                if version == 4:
                    vcard_map[
                        key
                    ] = f"{key};data:{data_type[4]};base64,{contact[value]}"
            continue

        # Handle all other scenarios
        try:
            data = contact[value]
        except (KeyError, TypeError):
            print(f"1004: CSV file has no key {value}")
            continue

        # Now check that we don't get garbage data
        if key == "GENDER":
            if data.upper() not in ["", "M", "F", "O", "N", "U"]:
                print(f"1006: Key {key} has invalid gender {data}")
            elif data:
                vcard_map[key] = f"{key}:{data.upper()}"
            continue
        elif key == "GEO":
            if not ";" in data:
                print(f"1007: Key {key} has invalid geo data {data}")
            elif data:
                vcard_map[key] = f"{key}:{data}"
        elif data:
            vcard_map[key] = f"{key}:{data}"

    # Actually add revision to our vcard if not exist
    try:
        vcard_map["REV"]
    except KeyError:
        vcard_map["REV"] = "REV:" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    vcard_str_content = ""
    for entry in vcard_map:
        vcard_str_content += vcard_map[entry] + "\n"

    # Foolproof check
    if vcard_map["FN"] == "FN:" or vcard_map["N"] == "N:;;;;;":
        print(f"1008: Cannot create vcard for contact {contact}")
        return None, None

    vcard = f"BEGIN:VCARD\nVERSION:{version}.0\n" + vcard_str_content + "END:VCARD\n"
    vc_filename = "-".join(filter(None, vcard_map["N"].split(";")))[2:] + ".vcf"

    return vcard, vc_filename
