import os
from csv2vcard.export_vcard import check_export_dir, export_vcard
from csv2vcard.create_vcard import create_vcard
from csv2vcard.parse_csv import parse_csv


def csv2vcard(csv_filename: str, csv_delimeter: str = ';', output_dir: str = None, single_vcard_file: bool = False) -> None:
    """
    Main function
    """
    check_export_dir(output_dir)

    vcards = ""
    for contact in parse_csv(csv_filename, csv_delimeter):
        vcard, filename = create_vcard(contact)
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
