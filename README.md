[![Downloads](http://pepy.tech/badge/csv2vcard)](http://pepy.tech/count/csv2vcard)

csv2vcard
=========
A Python script that parses a .csv file of contacts and automatically creates vCards. The vCards are super useful for sending your contact details or those of your team. You can also upload them to e.g. Dropbox and use them with QR codes! You can also use them for transferring new contacts to Outlook, a new CRM etc. The specific use case in mind was to programmatically create vCards from a list of contacts in a spreadsheet, to be incorporated into business cards.

Usage
-----

1. Install package with `pip3 install csv2vcard` installs the original package

1a. Install package with `pip install git+https://github.com/ReallyNameHere/csv2vcard.git@0.2.3` installs the package with the updated fields for  home address personal email & mobile

2. Create csv file with contacts

*CSV file format (delimeter can be changed in csv_delimeter param, see below)*

`last_name, first_name, org, title, phone, email, website, street, city, p_code, country`

**Important: you should NAME the columns EXCATLY the same way because they are used as keys to generate the vCards But it is not required to reorder the columns. This script will find the columns based on the NAME**

3. `cd yourcsvfoldername` go to the folder where you have your csv file

4. Open python `python3` (gotcha: using Python 3.6 features)

5. Import module `from csv2vcard import csv2vcard`

6. Now you have 2 options for running (both will create an /export/ dir for your vCard):

- Test the app with `csv2vcard.test_csv2vcard()`. This will create a Forrest Gump test vCard.
- Use your real data `csv2vcard.csv2vcard("yourcsvfilename", ",")` where ","  is your csv delimeter. This will create all your vCards.
