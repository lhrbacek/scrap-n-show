from urllib.request import urlopen
import json
import psycopg2

def fetch_data():
    flats_json = urlopen('https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=5000&tms=1663433765480')
    flats = json.loads(flats_json.read().decode("utf-8"))

    flats_db = []
    for i in range(500):
        flats_db.append((flats["_embedded"]["estates"][i]["name"].replace('\xa0', ' '), flats["_embedded"]["estates"][i]["_links"]["images"][0]["href"]))
    return flats_db

def connect_create_fill(flats_db):
    create_sql = """
    CREATE TABLE IF NOT EXISTS flats_info (
        title VARCHAR(255) NOT NULL,
        img_url VARCHAR(255)
    )
    """
    insert_sql = "INSERT INTO flats_info (title, img_url) VALUES(%s, %s)"

    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="flats",
            user="postgres",
            password="flats")

        cur = conn.cursor()
        cur.execute(create_sql)
        cur.executemany(insert_sql, flats_db)
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    flats_db = fetch_data()
    connect_create_fill(flats_db)
