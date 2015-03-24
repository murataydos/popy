===========
popy
===========

.. image:: https://pypip.in/d/popy/badge.png
  :target: https://pypi.python.org/pypi/popy/
.. image:: https://pypip.in/license/popy/badge.png
  :target: https://pypi.python.org/pypi/popy/
.. image:: https://travis-ci.org/murataydos/popy.svg
  :target: https://travis-ci.org/murataydos/popy/
.. image:: https://coveralls.io/repos/murataydos/popy/badge.svg 
  :target: https://coveralls.io/r/murataydos/popy
  
Parser for GNU Po files

Installation
============

Install using pip::

    pip install popy


Usage
============

Using popy to parse a PO file::

    from popy.po_file import PoFile  
  
    f = PoFile(path='/path/to/your/file.po')
    messages = f.get_messages() # gets all the messages  
    messages[0]
    # MessageEntry object
    messages[0].msgid
    # First message's msgid
    messages[1].msgstr
    # Second message's msgstr as a list
    
    
MessageEntry object
-------------------
These are the attributes::

    msgid: str
    msgstr: list of strings  
    msgid_plural: str  
    msgctxt: str  
    translator_comments: list of strings  
    extracted_comments: list of strings  
    references: list of strings  
    flags: list of strings  
    is_fuzzy: boolean
  
These are the important methods::

    fix_newline_matching() 
    # Adds or removes newlines to/from msgstr in order to match msgid and msgstr newlines at the beginning or end.
    
    __str__()
    # Generates a message block
    
    
PoFile object
-------------------
These are the attributes::

    path: str
    messages: list of MessageEntry objects  
  
These are the important methods::

    get_messages()
    # Reads messages and returns list of MessageEntry objects

    write_messages()
    # Writes MessageEntry objects into the file

    fix_newline_matching() 
    # Applys fix_newline_matching to the whole file
    
    __str__()
    # Generates a message block
