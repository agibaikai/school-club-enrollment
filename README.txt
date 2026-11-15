SCHOOL CLUB ENROLLMENT

RUN ON WINDOWS
1. Extract this entire ZIP archive.
2. Open the School_Clubs_Project folder in VS Code.
3. Open Terminal > New Terminal.
4. Run: py app.py
   If your Python command is python, run: python app.py
5. Open http://127.0.0.1:8000 in Chrome.
6. Press Ctrl+C in the terminal to stop the application.

Python 3 is required. No extra Python packages are needed.
The included SQLite database contains fictional demonstration data.

TRY THE APPLICATION
Student 101 can enroll in Robotics or Debate.
Student 102 is already enrolled in Robotics.
Drawing is full.
Unknown student IDs are rejected.
Submitting the same enrollment twice does not create duplicates.
Enrollment persists after restarting the application.
The student ID identifies a demo student. This local prototype has no login.

DATABASE ASSESSMENT
Open school_clubs.db with DB Browser for SQLite.
schema.sql contains three related tables with primary and foreign keys.
seed.sql inserts four students, three clubs and three enrollments.
search.sql uses AND and OR in one WHERE clause.
The original search returns Robotics (1 free place) and Debate (2 free places).

To demonstrate creation and insertion, create a NEW empty database,
run schema.sql and seed.sql in its Execute SQL tab, and take screenshots
showing the statements and results. Then run search.sql and capture its
query and result. The existing database already contains these tables.
Use the fresh demonstration database for reproducible initial results.

FILES
app.py: local HTTP server, validation and enrollment logic.
styles.css: page appearance.
school_clubs.db: initialized SQLite database.
schema.sql, seed.sql, search.sql: executable SQL.
SQL_Results.txt: actual output from executing these SQL files.
School_Clubs_Documentation.docx: English project documentation.

To reset demo data, stop the application, rename school_clubs.db as a backup,
and restart app.py. A fresh database is created automatically.
