# JLMP
!!!JLMP will NOT function on its own. Get the frontend here: <https://github.com/owmyeyesturnondarkmode/jlmp-frontend>!!!

**J**'s **L**ibrary **M**anagment **P**rogram
## What?
JLMP is a backend for library managment software, being able to:
- Initialize a library
- Add a book
- Remove a book
- Loan a book to a patron
- Return a book
- Add a Patron
- Remove a patron
- List loans that a patron has taken out
- Renew a loan
- Search the library catalog
- Get a book's info (such as title, date published, genre, and others)
- Get a patron's info

More features will be added, and the ones that I'm planning to add are listed below.
- More data for books
  - Subgenre, editon, etc.
- List a patron's overdue books
- List all overdue books
- Database snapshotting
- More will be added and removed from this list as time goes on
## Why?
One day, I was thinking: *Is there really a lot of library managment softwares out there?* And I decided that there probably weren't
too many. And then the big thing hit me: *But are they open-source?* And, me being me, without doing any research as to if they are
open source, decided to give the world an open-source library managment software.
## How?
### Data Storage
JLMP functions primarialy on XML. The library catalog, the patron catalog, and the list of checked out books are all XML. An
example of a book being stored on the library catalog is this:
```
<database>
  <book barcode="123456">
    <title>Harry Potter and the Deathly Hollows</title>
    <author>J. K. Rowling</author>
    <year>2007</year>
    <isbn>978-0-545-13970-0</isbn>
    <genre>fantasy</genre>
    <fiction>True</fiction>
  </book>
</database>
```
Patron data is stored like this:
```
<database>
  <patron card_num="1234">
    <name>John Doe</name>
    <email>johndoe@gmail.com</email>
    <phone>123-456-7890</phone>
    <notes><notes/>
</patron>
</database>
```
Loans are not stored in the patron's <patron> block, but instead stored in a seprerate file where the card number of the patron is attached.
Like this:
```
<database>
  <loan barcode="000000">
    <patron>1234</patron>
    <date>2026-04-04T19:59:51.967613</date>
    <due_date>2026-04-18T19:59:51.967662</due_date>
    <renewals>0</renewals>
  </loan>
</database>
```
### Syntax
| Function | Syntax |
| -------- | ------ |
| Initialize | `JLMP.library.init(barcode_length:str,loan_period:str)` |
| Add book | `JLMP.book.add(title:str, fiction:bool,genre:str,author:str, year:str, isbn:str)` |
| Remove book | `JLMP.book.remove(barcode:str)` |
| Loan book | `JLMP.book.loan(barcode:str, patron:str)` |
| Return book | `JLMP.book.return_loan(barcode:str)` |
| Add patron | `JLMP.patron.add(card_num:str,name:str, email:str, phone:str, notes:str)` |
| Remove patron | `JLMP.patron.remove(card_num:str)` |
| List patron's loans | `JLMP.patron.list_loans(card_num:str)` |
| Renew Loan | `JLMP.book.renew_loan(barcode:str)` |
| Search catalog | `JLMP.library.search(type:str,query:str)` (type: title, author, year, genre, isbn) |
| Get book info | `JLMP.book.get_info(barcode:str)` |
| Get patron info | `JLMP.patron.get_info(card_num:str)` |
