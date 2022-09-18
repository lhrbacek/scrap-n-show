import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_flats():
    select_sql = "SELECT title, img_url FROM flats_info"

    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="flats",
            user="postgres",
            password="flats")

        cur = conn.cursor()
        cur.execute(select_sql)
        rows = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        flats = get_flats()

        self.wfile.write(bytes("<html><head><title>Flats</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        for i in range(500):
            self.wfile.write(bytes("<p>{}</p>".format(flats[i][0]), "utf-8"))
            self.wfile.write(bytes("<img src={} alt=img width=\"300\" height=\"300\">".format(flats[i][1]), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8080), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
