import sqlite3

inputDataclothing = ['name', 'dob', 'pancard', 'gst_number', 'address', 'business_name', 'trade_license', 'udyam', 'account_number', 'ifsc_code', 'upi_id',  'noc', 'phoneNumber']

def store_data_clothing(kwargs):

    conn = sqlite3.connect('database.db')
    name = kwargs.get('name')
    dob = kwargs.get('dob')
    pancard = kwargs.get('pancard')
    gst_number = kwargs.get('gst_number')
    address = kwargs.get('address')
    business_name = kwargs.get('business_name')
    trade_license = kwargs.get('trade_license')
    udyam = kwargs.get('udyam')
    account_number = kwargs.get('account_number')
    ifsc_code = kwargs.get('ifsc_code')
    upi_id = kwargs.get('upi_id')
    noc = kwargs.get('noc')
    phoneNumber = kwargs.get('phoneNumber')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clothing (
        name TEXT,
        dob TEXT,
        pancard TEXT,
        gst_number TEXT,
        address TEXT,
        business_name TEXT,
        trade_license TEXT,
        udyam TEXT,
        account_number TEXT,
        ifsc_code TEXT,
        upi_id TEXT,
        noc TEXT,
        phoneNumber TEXT PRIMARY KEY)''')

    c.execute("INSERT INTO clothing (name, dob, pancard, gst_number, address, business_name, trade_license, udyam, account_number, ifsc_code, upi_id, noc, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, dob, pancard, gst_number, address, business_name, trade_license, udyam, account_number, ifsc_code, upi_id, noc, phoneNumber))
    conn.commit()
    conn.close()

def send_message_clothing(data_type):
    msg = ""

    match data_type:
        case 'name':
            msg = "Please enter your name:"
        case 'dob':
            msg = "Please enter your date of birth:"
        case 'pancard':
            msg = "Please enter your pancard number:"
        case 'gst_number':
            msg = "Please enter your GST number:"
        case 'address':
            msg = "Please enter your address:"
        case 'business_name':
            msg = "Please enter your business name:"
        case 'trade_license':
            msg = "Please enter your trade license number:"
        case 'udyam':
            msg = "Please enter your udyam number:"
        case 'account_number':
            msg = "Please enter your account number:"
        case 'ifsc_code':
            msg = "Please enter your IFSC code:"
        case 'upi_id':
            msg = "Please enter your UPI ID:"
        case 'noc':
            msg = "Please enter your NOC number:"
        case 'phoneNumber':
            msg = "Please enter your phone number:"

    return msg
