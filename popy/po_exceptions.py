

class InvalidMessageEntry(Exception):
    """
    Raised when parser fail to parse a message entry
    """
    pass

class InvalidFilePath(Exception):
	"""
	Raised when parser can't find the po file
	"""
	pass
