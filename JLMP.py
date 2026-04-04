# J's library managment system

import os
import xml.etree.ElementTree as ET

homedir = os.path.expanduser("~/.local/share/wls/")
debug = True
if debug:
    homedir = "./debug/"

class JLMP:
    def init(barcode_length:str):
        try:
            os.makedirs(homedir, exist_ok=False)
        except OSError:
            return FileExistsError.add_note("Already initialized.")
        if barcode_length.isdigit():
            barcode_length = int(barcode_length)
            if 3 <= barcode_length <= 10:
                os.system(f"touch {homedir}settings.xml")
                with open(f"{homedir}settings.xml", "w") as f:
                    f.write(f"<settings><barcode_length>{barcode_length}</barcode_length></settings>")
            else:
                os.system(f"touch {homedir}settings.xml")
                with open(f"{homedir}settings.xml", "w") as f:
                    f.write("<settings><barcode_length>6</barcode_length></settings>")
        else:
            os.system(f"touch {homedir}settings.xml")
            with open(f"{homedir}settings.xml", "w") as f:
                f.write("<settings><barcode_length>6</barcode_length></settings>")
        os.makedirs(f"{homedir}database/", exist_ok=True)
        with open(f"{homedir}database/library.xml", "w") as f:
            f.write("<database></database>")
        with open(f"{homedir}database/barcodes", "w") as f:
            f.write("")

    def add_book(title:str, author:str, year:str, isbn:str):
        if not os.path.exists(f"{homedir}settings.xml"):
            return FileNotFoundError.add_note("Please initialize the library first.")
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

        book_element = ET.SubElement(library_root, barcode)
        ET.SubElement(book_element, "title").text = title
        ET.SubElement(book_element, "author").text = author
        ET.SubElement(book_element, "year").text = year
        ET.SubElement(book_element, "isbn").text = isbn
        library_tree.write(library_path)