def create_vcard(contact: dict):
    """
    The mappings used below are from https://www.w3.org/TR/vcard-rdf/#Mapping
    """
    vc_begin = "BEGIN:VCARD\n"
    vc_version = "VERSION:3.0\n"
    vc_name = f"N;CHARSET=UTF-8:{contact['last_name']};{contact['first_name']};;;\n"
    vc_title = f"TITLE;CHARSET=UTF-8:{contact['title']}\n"
    vc_org = f"ORG;CHARSET=UTF-8:{contact['org']}\n"
    vc_phone = f"TEL;TYPE=WORK,VOICE:{contact['phone']}\n"
    vc_email = f"EMAIL;TYPE=WORK:{contact['email']}\n"
    vc_website = f"URL;TYPE=WORK:{contact['website']}\n"
    vc_address = f"ADR;TYPE=WORK;CHARSET=UTF-8:{contact['street']};{contact['city']};{contact['p_code']};{contact['country']}\n"
    #These fields have been added to the original code
    vc_phone_cell = f"TEL;TYPE=CELL,VOICE:{contact['phone_cell']}\n"
    vc_email_home = f"EMAIL;TYPE=HOME:{contact['email_home']}\n"
    vc_bday = f"BDAY;CHARSET=UTF-8:{contact['bday']}\n"
    vc_note = f"NOTE;CHARSET=UTF-8:{contact['note']}\n"
    #end of new fields
    vc_end = "END:VCARD\n"
    

    vc_filename = f"{contact['last_name'].lower()}_{contact['first_name'].lower()}.vcf"
    #I added to this line below
    vc_output = vc_begin + vc_version + vc_name + vc_title + vc_org + vc_phone + vc_email + vc_website + vc_address + vc_phone_cell + vc_email_home + vc_bday + vc_note + vc_end

    vc_final = {
        "filename" : vc_filename,
        "output" : vc_output,
        "name" : contact['first_name'] + contact['last_name'],
    }

    return vc_final
