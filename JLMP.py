# J's library managment system

import os
import xml.etree.ElementTree as ET
import datetime

homedir = "./JLMP/"

class JLMP:
    def init(barcode_length:str,loan_period:str):
        try:
            os.makedirs(homedir, exist_ok=False)
        except OSError:
            raise FileExistsError
        if barcode_length.isdigit():
            barcode_length = int(barcode_length)
            if 3 <= barcode_length:
                os.system(f"touch {homedir}settings.xml")
                with open(f"{homedir}settings.xml", "w") as f:
                    f.write(f"<settings><barcode_length>{barcode_length}</barcode_length></settings>")
            else:
                raise ValueError
        else:
            raise ValueError

        if loan_period.isdigit():
            loan_period = int(loan_period)
            if loan_period > 1:
                with open(f"{homedir}settings.xml", "r") as f:
                    settings_tree = ET.parse(f)
                    settings_root = settings_tree.getroot()
                ET.SubElement(settings_root, "loan_period").text = str(loan_period)
                settings_tree.write(f"{homedir}settings.xml")
            else:
                raise ValueError
        os.makedirs(f"{homedir}database/", exist_ok=True)
        with open(f"{homedir}database/library.xml", "w") as f:
            f.write("<database></database>")
        with open(f"{homedir}database/barcodes", "w") as f:
            f.write("")
        with open(f"{homedir}database/loans.xml", "w") as f:
            f.write("<database></database>")
        with open(f"{homedir}database/patrons.xml", "w") as f:
            f.write("<database></database>")

    def add_book(title:str, fiction:bool,genre:str,author:str, year:str, isbn:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        settings_tree = ET.parse(f"{homedir}settings.xml")
        settings_root = settings_tree.getroot()
        barcode_length = int(settings_root.find("barcode_length").text)
        barcode_path = f"{homedir}database/barcodes"
        with open(barcode_path, "r+") as f:
            last_barcode = f.read().strip()
            if last_barcode == "":
                barcode = "0" * barcode_length
            else:
                barcode = str(int(last_barcode) + 1).zfill(barcode_length)
            f.seek(0)
            f.truncate()
            f.write(barcode)
        library_path = f"{homedir}database/library.xml"
        try:
            library_tree = ET.parse(library_path)
            library_root = library_tree.getroot()
        except ET.ParseError:
            library_root = ET.Element("database")
            library_tree = ET.ElementTree(library_root)
        book_element = ET.SubElement(library_root, "book", {"barcode": barcode})
        ET.SubElement(book_element, "title").text = title
        ET.SubElement(book_element, "author").text = author
        ET.SubElement(book_element, "year").text = year
        ET.SubElement(book_element, "isbn").text = isbn
        ET.SubElement(book_element, "genre").text = genre
        ET.SubElement(book_element, "fiction").text = str(fiction)
        library_tree.write(library_path)

    def rem_book(barcode:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        library_path = f"{homedir}database/library.xml"
        try:
            library_tree = ET.parse(library_path)
            library_root = library_tree.getroot()
        except ET.ParseError:
            raise ValueError
        book_element = library_root.find(f"book[@barcode='{barcode}']")
        if book_element is None:
            raise ValueError
        library_root.remove(book_element)
        library_tree.write(library_path)

    def loan_book(barcode:str, patron:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        library_path = f"{homedir}database/library.xml"
        try:
            library_tree = ET.parse(library_path)
            library_root = library_tree.getroot()
        except ET.ParseError:
            raise ValueError
        book_element = library_root.find(f"book[@barcode='{barcode}']")
        if book_element is None:
            raise ValueError
        loans_path = f"{homedir}database/loans.xml"
        try:
            loans_tree = ET.parse(loans_path)
            loans_root = loans_tree.getroot()
        except ET.ParseError:
            loans_root = ET.Element("database")
            loans_tree = ET.ElementTree(loans_root)
        settings_path = f"{homedir}settings.xml"
        settings_tree = ET.parse(settings_path)
        settings_root = settings_tree.getroot()
        loan_element = ET.SubElement(loans_root, "loan", {"barcode": barcode})
        ET.SubElement(loan_element, "patron").text = patron
        ET.SubElement(loan_element, "date").text = datetime.datetime.now().isoformat()
        ET.SubElement(loan_element, "due_date").text = (datetime.datetime.now() + datetime.timedelta(days=int(settings_root.find("loan_period").text))).isoformat()
        ET.SubElement(loan_element, "renewals").text = "0"
        loans_tree.write(loans_path)

    def return_book(barcode:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        loans_path = f"{homedir}database/loans.xml"
        try:
            loans_tree = ET.parse(loans_path)
            loans_root = loans_tree.getroot()
        except ET.ParseError:
            raise ValueError
        loan_element = loans_root.find(f"loan[@barcode='{barcode}']")
        if loan_element is None:
            raise ValueError
        loans_root.remove(loan_element)
        loans_tree.write(loans_path)
    
    def add_patron(card_num:str,name:str, email:str, phone:str, notes:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        patrons_path = f"{homedir}database/patrons.xml"
        try:
            patrons_tree = ET.parse(patrons_path)
            patrons_root = patrons_tree.getroot()
        except ET.ParseError:
            patrons_root = ET.Element("database")
            patrons_tree = ET.ElementTree(patrons_root)
        patron_element = ET.SubElement(patrons_root, "patron", {"card_num": card_num})
        ET.SubElement(patron_element, "name").text = name
        ET.SubElement(patron_element, "email").text = email
        ET.SubElement(patron_element, "phone").text = phone
        ET.SubElement(patron_element, "notes").text = notes
        patrons_tree.write(patrons_path)

    def rem_patron(card_num:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        patrons_path = f"{homedir}database/patrons.xml"
        try:
            patrons_tree = ET.parse(patrons_path)
            patrons_root = patrons_tree.getroot()
        except ET.ParseError:
            raise ValueError
        patron_element = patrons_root.find(f"patron[@card_num='{card_num}']")
        if patron_element is None:
            raise ValueError
        patrons_root.remove(patron_element)
        patrons_tree.write(patrons_path)

    def list_loans(card_num:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        loans_path = f"{homedir}database/loans.xml"
        try:
            loans_tree = ET.parse(loans_path)
            loans_root = loans_tree.getroot()
        except ET.ParseError:
            raise ValueError
        patron_loans = []
        for loan in loans_root:
            if loan.find("patron").text == card_num:
                patron_loans.append(loan.get("barcode"))
        return patron_loans
    
    def renew_loan(barcode:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        loans_path = f"{homedir}database/loans.xml"
        try:
            loans_tree = ET.parse(loans_path)
            loans_root = loans_tree.getroot()
        except ET.ParseError:
            raise ValueError
        loan_element = loans_root.find(f"loan[@barcode='{barcode}']")
        if loan_element is None:
            raise ValueError
        settings_path = f"{homedir}settings.xml"
        settings_tree = ET.parse(settings_path)
        settings_root = settings_tree.getroot()
        due_date = datetime.datetime.fromisoformat(loan_element.find("due_date").text)
        new_due_date = due_date + datetime.timedelta(days=int(settings_root.find("loan_period").text))
        loan_element.find("due_date").text = new_due_date.isoformat()
        loan_element.find("renewals").text = str(int(loan_element.find("renewals").text) + 1)
        loans_tree.write(loans_path)

    def search(type:str,query:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        if type not in ["title", "author", "genre", "year", "isbn"]:
            raise ValueError
        library_path = f"{homedir}database/library.xml"
        try:
            library_tree = ET.parse(library_path)
            library_root = library_tree.getroot()
        except ET.ParseError:
            library_root = ET.Element("database")
            library_tree = ET.ElementTree(library_root)
        results = []
        for book in library_root:
            if query.lower() in book.find(f"{type}").text.lower():
                results.append(JLMP.get_book_info(book))
        return results

    def get_book_info(barcode:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            raise FileNotFoundError
        library_path = f"{homedir}database/library.xml"
        try:
            library_tree = ET.parse(library_path)
            library_root = library_tree.getroot()
        except ET.ParseError:
            library_root = ET.Element("database")
            library_tree = ET.ElementTree(library_root)
        book_element = library_root.find(f"book[@barcode='{barcode}']")
        if book_element is None:
            raise ValueError
        return f"{barcode.get('barcode')}: {barcode.find('title').text} | {barcode.find('genre').text} | {barcode.find('author').text} | {barcode.find('year').text}) | Fiction: {barcode.find('fiction').text}"

if __name__ == "__main__":
    print("This is not a frontend, it will not do anything when run on its own.\n" \
    "Please download the frontend from github, or get a 3rd-party one to interface\n" \
    "with this app. Alternatively, if you know about the internals of this app,\n" \
    "you can run 'python3' in a terminal, then import this file and interface with\n" \
    "it directly.")
    input("\nPress enter to exit.")