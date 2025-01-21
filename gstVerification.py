import re

def isGST_number(str):

	regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$"

	p = re.compile(regex)

	if (str == None):
		return False

	if(re.search(p, str)):
		return True
	else:
		return False
