[![Downloads](http://pepy.tech/badge/csv2vcard)](http://pepy.tech/count/csv2vcard)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/netinvent/csv2vcard.svg)](http://isitmaintained.com/project/netinvent/csv2vcard "Percentage of issues still open")
[![GitHub Release](https://img.shields.io/github/release/netinvent/csv2vcard.svg?label=Latest)](https://github.com/netinvent/csv2vcard/releases/latest)
[![Windows linter](https://github.com/netinvent/csv2vcard/actions/workflows/pylint-windows.yaml/badge.svg)](https://github.com/netinvent/csv2vcard/actions/workflows/pylint-windows.yaml)
[![Linux linter](https://github.com/netinvent/csv2vcard/actions/workflows/pylint-linux.yaml/badge.svg)](https://github.com/netinvent/csv2vcard/actions/workflows/pylint-linux.yaml)

# csv2vcard

A Python script that parses a .csv file of contacts and automatically creates vCards. The vCards are useful for sending your contact details or those of your team. You can also upload them to e.g. Dropbox and use them with QR codes! You can also use them for transferring new contacts to Outlook, a new CRM etc. The specific use case in mind was to programmatically create vCards from a list of contacts in a spreadsheet, to be incorporated into business cards.

As of 0.6.0, csv2vcard has the following new capabilities:
- CLI and GUI interfaces
  - Native Windows support through prebuilt executables
  - Linux support through pip with shell script `csv2vcard-cli`
- supports both vCards version 3.0 and 4.0 (default)
- Autodetects file encoding
- Can use custom CSV mapping files, with nested values mapping
- Generate a single vCard file containing all contacts from a CSV file
  - Can split single vCard file into smaller chunks for webmails that don't like them (eg Grommunio 2023.11 does not accept more than about 80kb per file)
- Supports Logo, Photo and PGP vCard keys as links or inline base64
- Parse multiple CSV files when directory given
- Optionally remove accents from vCards
- Basic data validation
- GUI Settings import and export for quick pre-configuration

## Usage

### Windows usage

Download the pre-built executable directly from the [release page](https://github.com/netinvent/csv2vcard/releases)  
Download the optional mappings or settings files, and you're set to go.

![image](.github/img/gui-0.6.0.png)

### Linux / Windows / MacOS X usage

Requirements: Runs on Linux, Windows (and probably macos too), using Python 3.6+

1. Install **this updated** package with `pip install git+https://github.com/netinvent/csv2vcard.git@0.6.1` (package with all new fancy stuff)

Once installed, the scripts `csv2vcard-cli` and `csv2vcard-gui` will be available. Note that you'll need to install extra requirements for the GUI to work, namely `pip install PySimpleGUI ofunctions.threading`

2. Accepted CSV file format

Any CSV file format is accepted using custom mappings (see below)  
By default, the following columns are recognized:  

`"postbox_home","address_home","city_home","region_home","zip_home","country_home","postbox","address","city","region","zip","country", "anniversary","birthday","categories","email_home","email","title","last_name","first_name","gender","geo","key",logo","last_name","first_name", "second_name", "title","suffix","remarks","nickname","company","photo","role","fax_home","pager_home","phone_home","video_phone_home","text_phone_home","text_home","mobile_phone","fax","pager","phone","video_phone","text_phone","text","title","timezone","uuid","webpage"`

There's no need for those columns to be in a specific order for the script to work, as long as they are spelled right.  

*CSV file format (delimeter can be changed in csv_delimeter param, see below)*

3. Run program with `csv2vcard-cli -s /path/to/csv/file.csv -o /path/to/output_dir`


## Advanced usage

`csv2vcard-cli` accepts the following custom parameters:

| Parameter                                          | Role                                                       |
|----------------------------------------------------|------------------------------------------------------------|
| -s|--source <path to dir or file>                  | Adds one or multiple (recursive) CSV files to job          |
| -o|--output <path to output directory>             | Specifies the path where to store vCard files              |
| --h|--help                                         | Shows help                                                 |
| --delimiter <any single character like `;`, `,`>   | Changes default delimiter `;`                              |
| --single-vcard                                     | Creates a single vCard file containing all the contacts    |
| --max-vcard-file-size <integer>                    | Limits single vCard files to max (kb) size                 |
| --max-vcards-per-file <integer>                    | Limits single vCard files to maximium vcards               |
| --vcard-version <3|4>                              | Chooses which vCard version to generate (defaults to 4)    |
| --encoding <python known encoding string>          | Replaces automagically detected file encoding              |
| -m|--mapping <path_to_json_mapping_file>           | Replaces default mapping with custom one (see below)       |
| --strip-acccents                                   | Removes any accents from vCard, for max compatibility      |

## Custom mappings

By default, the CSV columns mentionned earlier are all mapped to vCards.  
csv2vcard supports custom vCard mappings, that can have nested values or multiple mappings.  
Mapping are written in JSON, and represent a dictionnary of vCard keys, with values being corresponding CSV column names.

The default mapping included in csv2vcard looks like the following:
```
{
    "ADR": {
        "TYPE": {
            "HOME": ["postbox_home", "address_home", "city_home", "region_home", "zip_home", "country_home"],
            "WORK": ["postbox", "address", "city", "region", "zip", "country"],
        }
    },
    "ANNIVERSARY": "anniversary",
    "BDAY": "birthday",
    "CATEGORIES": "categories",
    "EMAIL": 
        {"TYPE":
            {"HOME": 
                "email_home", 
                "WORK": "email"
            }
        },
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
```

Since vCard has nested values, the mapping file needs to be nested too.  
Some values like FormattedName (`FN`) can be string concatenations. In our case, the CSV fields `Title`, `FirstName` and `LastName` will be concatenated into the `FN` property. Concatenations must use the form:
```
    "FN": {"CONCAT": ["Title", "FirstName", "LastName]}
```

Other properties must concatenate columns with a separator, just as the Name (`N`) property. They must use the following syntax, representing each CSV column that shall be used in a list:
```
    "N": ["last_name", "first_name", "second_name", "title", "suffix"],
```
The order of the above list follows the syntax of vCard standards.

You can create our own custom mapping to read your random CSV file provider format.
An example of Orange Business webmail CSV exports can be found in the mappings directory of this project

** If you make a good mapping for a known service (eg Outlook, gmail, yahoo...), please make a pull request or simply post them in an issue so I can add it to the mappings directory, Thanks**

## Inline base64

Photo, Logo and (PGP)Key properties can be set to link to an URI (needs to begin with http(s)), or could be set to incorporate directly base64 encoded data. In that case, your CSV file will be very long, but csv2vcard will handle this scenario too.
If you can, just put those columns at the end of the file for better readability.

## Data validation

Empty columns won't trigger any errors unless there's no FN or N properties that can be generated.  
Simple checks are performed on:
- KEY, LOGO and PHOTO properties (check if begins with http(s) or if value is base64 encoded)
- GENDER which required to be a single character according to vCard standard
- GEO which requires to be two floats separated by a semi-column
- EMAIL which will check email address against RFC822


## Examples

#### Convert an Orange webmail CSV export to vCards compatible with Grommunio web import (max 80kb size without accents)  
- GUI
Convert an Orange webmail CSV export to Grommunio compatible single vCard files
![image](.github/img/gui-example-orange-webmail-config.png)

- On Windows CLI
```
csv2vcard.cmd -s "c:\contacts" -o "c:\contacts\vcards" --single-vcard -m mappings\orange_webmail.json --delimiter , --max-vcards-per-file 490 --strip-accents
```
- On Linux CLI
```
csv2vcard -s /contacts -o /contacts/vcards --single-vcard -m /opt/mappigs/orange_webmail.json --delimiter , --max-vcards-per-file 490 --strip-accents
```
