#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of csv2vcard module

"""
Versioning semantics:
    Major version: backward compatibility breaking changes
    Minor version: New functionality
    Patch version: Backwards compatible bug fixes
"""

__intname__ = "tests.create_vcard"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2023 NetInvent SASU"
__licence__ = "MIT"
__build__ = "2023112401"

from csv2vcard.csv_handler import *


def test_csv2vcard(version: int = 4):
    """
    Try it out with this mock Forrest Gump contact
    """
    mock_contacts = [
        {
            "last_name": "Gump",
            "first_name": "Forrest",
            "title": "Shrimp Man",
            "org": "Bubba Gump Shrimp Co.",
            "phone": "+49 170 5 25 25 25",
            "email": "forrestgump@example.com",
            "website": "https://www.linkedin.com/in/forrestgump",
            "street": "42 Plantation St.",
            "city": "Baytown",
            "p_code": "30314",
            "country": "United States of America",
            "phone_cell": "+19177777777",
            "email_home": "forrestgump@examplehome.com",
            "street_home": "600 Main St.",
            "city_home": "Brooklynn",
            "p_code_home": "13458",
            "country_home": "USA",
            "bday": "12/03/1965",
            "note": "This works!!!!!!!!",
        }
    ]

    output_dir = "."
    check_export_dir(output_dir)
    vcard, filename = create_vcard(mock_contacts[0], version)
    print(vcard)
    export_vcard(vcard, output_dir, filename)

if __name__ == "__main__":
    print("Example code for %s, %s" % (__intname__, __build__))
    test_csv2vcard()
