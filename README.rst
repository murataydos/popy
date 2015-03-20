===========
popy
===========

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
  
These are the important methods::

    fix_newline_matching() 
    # Adds or removes newlines to/from msgstr in order to match msgid and msgstr newlines at the beginning or end.
    
    __str__()
    # Generates a message block
  

