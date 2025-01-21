import re

def isPAN_number(pan):
    regex = "^[A-Z]{3}[PCHFATBLJG][A-Z][0-9]{4}[A-Z]$"

    p = re.compile(regex)

    if (pan == None):
        return False
    
    if(re.search(p, pan)):
        return True
    else:
        return False
