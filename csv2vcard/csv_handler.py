import os
from csv2vcard.export_vcard import check_export_dir, export_vcard
from csv2vcard.create_vcard import create_vcard
import csv
import codecs


def parse_csv(csv_filename: str, csv_delimiter: str):
    """
    Simple csv parser with a ; delimiter
    """
    print("Parsing csv..")
    try:
        with open(f"{csv_filename}", "r", encoding="utf-8") as fh:
            contacts = csv.reader(fh, delimiter=csv_delimiter)
            header = next(contacts)  # saves header
            parsed_contacts = [dict(zip(header, row)) for row in contacts]
            return parsed_contacts
    except OSError as exc:
        print(f"OS error for {csv_filename}: {exc}")
        return []


def csv2vcard(csv_filename: str, csv_delimiter: str = ';', output_dir: str = None, vcard_version: int = 4, single_vcard_file: bool = False) -> None:
    """
    Main function
    """
    check_export_dir(output_dir)

    vcards = ""
    for contact in parse_csv(csv_filename, csv_delimiter):
        vcard, filename = create_vcard(contact, vcard_version)
        if single_vcard_file:
            export_vcard(vcard, output_dir, filename)
        else:
            vcards += "\n" + vcard['content']
    if not single_vcard_file:
        export_vcard(vcards, output_dir, os.path.basename(csv_filename) + ".vcf")

def test_csv2vcard(version: int = 4):
    """
    Try it out with this mock Forrest Gump contact
    """
    mock_contacts = [{
        "last_name": "Gump", "first_name": "Forrest", "title": "Shrimp Man",
        "org": "Bubba Gump Shrimp Co.",
        "phone": "+49 170 5 25 25 25", "email": "forrestgump@example.com",
        "website": "https://www.linkedin.com/in/forrestgump",
        "street": "42 Plantation St.", "city": "Baytown", "p_code": "30314",
        "country": "United States of America",
        "phone_cell": "+19177777777",
        "email_home": "forrestgump@examplehome.com",
        "street_home": "600 Main St.", "city_home": "Brooklynn", "p_code_home": "13458",
        "country_home": "USA",
        "bday": "12/03/1965",
        "note": "This works!!!!!!!!"
    }]
    
    output_dir = "."
    check_export_dir(output_dir)
    vcard, filename = create_vcard(mock_contacts[0], version)
    print(vcard)
    export_vcard(vcard, output_dir, filename)
