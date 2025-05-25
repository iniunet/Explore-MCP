import sqlite3 as db

COMM_DB='z:/comm.db'

def dbconnect():
    conn = db.connect(COMM_DB, check_same_thread=False)
    return conn

def get_close_4_comm(option_no):
    conn = dbconnect()
    c = conn.cursor()
    t = (option_no,)
    print(option_no)
    c.execute('select date,close from options_ticks where option_no=? order by date desc limit 1', t)
    for date, close in c:    
        print(date,' close from db is --',close)
    c.close()
    conn.close()
    price_dict={"date":date,"close":close}
    return price_dict
