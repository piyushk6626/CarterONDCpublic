import sqlite3

def get_data_by_phone(phone):
    data = {}
    for db_name in ['clothing', 'handicraft', 'kiriana', 'resturant']:
        conn = sqlite3.connect(f'{db_name}.db')
        c = conn.cursor()
        c.execute(f"SELECT name, business_name, gst_number, address FROM {db_name} WHERE phone_number = ?", (phone,))
        res = c.fetchone()
        if res:
            data[db_name] = {
                'name': res[0],
                'business_name': res[1],
                'gst_number': res[2],
                'address': res[3],
            }
        conn.close()
    return data
