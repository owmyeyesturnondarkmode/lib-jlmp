# JLMP 1.x.x API
The application's home directory is in `~/.local/share/wls`. This makes it incompatible with windows.
## Database
Everything in it's database is stored in an XML format. How books are stored in the DB is the following, and anything in square brackets should be replaced by that property of the book:
```
<database>
    <[barcode]>
        <title>[title]</title>
        <author>[author]</author>
        <year>[year]</year>
        <isbn>[isbn]</isbn>
    </[barcode]>
</database>
```