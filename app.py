"""School Club Enrollment. Run with Python 3. No third-party packages."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from html import escape
import sqlite3

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "school_clubs.db"

def connect():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize():
    if DATABASE.exists():
        return
    connection = connect()
    try:
        connection.executescript((ROOT / "schema.sql").read_text())
        connection.executescript((ROOT / "seed.sql").read_text())
    finally:
        connection.close()

def enroll(student_id, club_id):
    connection = connect()
    try:
        connection.execute("BEGIN IMMEDIATE")
        student = connection.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
        club = connection.execute("SELECT * FROM clubs WHERE club_id=?", (club_id,)).fetchone()
        if not student or not club:
            return "Please enter a valid student ID and select an existing club."
        existing = connection.execute(
            "SELECT enrollment_id FROM enrollments WHERE student_id=? AND club_id=?",
            (student_id, club_id)).fetchone()
        if existing:
            return "You are already enrolled in this club."
        count = connection.execute("SELECT COUNT(*) FROM enrollments WHERE club_id=?", (club_id,)).fetchone()[0]
        if count >= club["capacity"]:
            return "Club full. Please choose another club."
        cursor = connection.execute("INSERT INTO enrollments(student_id,club_id) VALUES (?,?)", (student_id,club_id))
        connection.commit()
        return f"Enrollment confirmed · {club['name']} · {club['schedule']} · Enrollment number {cursor.lastrowid}"
    finally:
        connection.close()

def page(message=""):
    connection = connect()
    try:
        clubs = connection.execute("""
            SELECT c.*, c.capacity-COUNT(e.enrollment_id) AS available
            FROM clubs c LEFT JOIN enrollments e ON c.club_id=e.club_id
            GROUP BY c.club_id ORDER BY c.club_id
        """).fetchall()
    finally:
        connection.close()
    cards = []
    for club in clubs:
        disabled = "disabled" if club["available"] == 0 else ""
        button = "Club full" if disabled else "Confirm enrollment"
        cards.append(f"""<article><p class="category">{escape(club['category'])}</p>
        <h2>{escape(club['name'])}</h2><p>{escape(club['schedule'])}</p>
        <p class="places">{club['available']} of {club['capacity']} places available</p>
        <form method="post" action="/enroll">
        <input type="hidden" name="club_id" value="{club['club_id']}">
        <label for="student-{club['club_id']}">Student ID</label>
        <input id="student-{club['club_id']}" name="student_id" type="number" min="1"
        required placeholder="e.g. 101" {disabled}>
        <button {disabled}>{button}</button></form></article>""")
    notice = f'<div class="notice" role="status">{escape(message)}</div>' if message else ''
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>School Club Enrollment</title><link rel="stylesheet" href="/styles.css"></head>
    <body><header><a href="/">School clubs</a><span>Find your next interest</span></header>
    <main><h1>Make time for<br>something you love.</h1>
    <p class="intro">Explore our clubs, check available places and enroll.</p>
    {notice}<section aria-label="Available clubs">{''.join(cards)}</section>
    <p class="help">Demo student IDs: 101, 102, 103, 104. Use 101 to try a new enrollment.</p>
    </main></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def send(self, content, content_type="text/html; charset=utf-8", status=200):
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        request = urlparse(self.path)
        if request.path == "/styles.css":
            self.send((ROOT / "styles.css").read_text(), "text/css")
        elif request.path == "/":
            message = parse_qs(request.query).get("message", [""])[0]
            self.send(page(message))
        else:
            self.send("Page not found", status=404)

    def do_POST(self):
        if self.path != "/enroll":
            self.send("Page not found", status=404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length <= 4096:
                self.send("Invalid request", status=400)
                return
            fields = parse_qs(self.rfile.read(length).decode("utf-8"))
            result = enroll(int(fields.get("student_id", [""])[0]),
                            int(fields.get("club_id", [""])[0]))
        except (ValueError, UnicodeDecodeError):
            result = "Please enter a valid numeric student ID."
        except sqlite3.Error:
            result = "Unable to complete enrollment. Please try again."
        from urllib.parse import urlencode
        self.send_response(303)
        self.send_header("Location", "/?" + urlencode({"message": result}))
        self.end_headers()

if __name__ == "__main__":
    initialize()
    print("Open http://127.0.0.1:8000 in your browser. Press Ctrl+C to stop.")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
