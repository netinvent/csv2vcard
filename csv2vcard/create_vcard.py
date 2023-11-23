from typing import Tuple

def create_vcard(contact: dict, version: int = 4) -> Tuple[str, str]:
    """
    The mappings used below are from https://www.w3.org/TR/vcard-rdf/#Mapping
    """

    if version not in [3, 4]:
        raise ValueError("Incorrect Vcard version given. Currently supported: 3 or 4.")
    elif version == 3:
        charset = ";CHARSET=UTF-8"
    else:
        charset = ""
    
    vc_begin = "BEGIN:VCARD\n"
    vc_version = f"VERSION:{version}.0\n"
    vc_name = f"N{charset}:{contact['last_name']};{contact['first_name']};;;\n"
    vc_title = f"TITLE{charset}:{contact['title']}\n"
    vc_org = f"ORG{charset}:{contact['org']}\n"
    vc_phone = f"TEL{charset};TYPE=WORK,VOICE:{contact['phone']}\n"
    vc_email = f"EMAIL{charset};TYPE=WORK:{contact['email']}\n"
    vc_website = f"URL{charset};TYPE=WORK:{contact['website']}\n"
    vc_address = f"ADR{charset};TYPE=WORK:{contact['street']};{contact['city']};{contact['p_code']};{contact['country']}\n"
    #These fields have been added to the original code
    vc_phone_cell = f"TEL{charset};TYPE=CELL,VOICE:{contact['phone_cell']}\n"
    vc_email_home = f"EMAIL{charset};TYPE=HOME:{contact['email_home']}\n"
    vc_address_home = f"ADR{charset};TYPE=HOME:{contact['street_home']};{contact['city_home']};{contact['p_code_home']};{contact['country_home']}\n"
    vc_bday = f"BDAY{charset}:{contact['bday']}\n"
    vc_note = f"NOTE{charset}:{contact['note']}\n"
    #end of new fields
    vc_end = "END:VCARD\n"
    

    vc_name = f"{contact['last_name']}_{contact['first_name']}"
    vc_filename = vc_name.lower() + ".vcf"
    #I added to this line below
    vcard = vc_begin + vc_version + vc_name + vc_title + vc_org + vc_phone + vc_email + vc_website + vc_address + vc_phone_cell + vc_email_home \
        + vc_address_home + vc_bday + vc_note + vc_end

    return vcard, vc_filename
