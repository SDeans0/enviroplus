import threading
import time
import collections
import sqlite3
from enviroplus import gas
from functools import partial

def read_data(q: collections.deque):
    while True:
        reading: gas.Mics6814Reading = gas.read_all()
        q.append((str(time.gmtime()), reading.oxidising, reading.reducing, reading.nh3))
        # threading.sleep(0.25)

def store_data(q: collections.deque):
    con = sqlite3.connect("readings.db")
    while True:
        data = []
        while q:
            data.append(q.popleft())
        if data:
            cur = con.cursor()
            cur.executemany("INSERT INTO readings VALUES (?,?,?,?)", data)
            con.commit()

def main():
    try:
        con = sqlite3.connect("readings.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE readings(time, ox, reducing, ammonia)")
        con.commit()
    except sqlite3.OperationalError:
        pass
    q = collections.deque()
    read = partial(read_data, q)
    store = partial(store_data, q)
    reader = threading.Thread(target=read)
    storer = threading.Thread(target=store)
    reader.start()
    storer.start()




if __name__ == "__main__":
    main()