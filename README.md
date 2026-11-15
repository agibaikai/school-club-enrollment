# School Club Enrollment

A school project about enrolling students in extracurricular clubs.

## Try the website

`index.html` is a static demo that can be hosted on Vercel. Open it in a browser or deploy the repository. Use sample student IDs `101`, `102`, `103`, or `104`.

The hosted demo stores enrollments in the current browser only. It does not send student information to a server. Use the **Reset demo** button to restore the initial sample places.

## Run the Python version locally

1. Install Python 3.
2. Open this folder in VS Code.
3. In the terminal, run `py app.py` (or `python app.py`).
4. Open `http://127.0.0.1:8000`.
5. Stop it with `Ctrl+C`.

The Python prototype uses the included SQLite database. The database contains fictional sample data and is separate from the Vercel demo.

## Database assessment files

- `schema.sql` creates the three related tables.
- `seed.sql` inserts sample students, clubs, and enrollments.
- `search.sql` uses `AND` and `OR` in one `WHERE` clause.
- `school_clubs.db` is the initialized SQLite database.

Open the database with DB Browser for SQLite. For screenshots showing table creation and inserts, create a separate empty database and execute `schema.sql`, then `seed.sql`, then `search.sql`.

## Files

- `index.html`, `styles.css`, `app.js`: static hosted demo.
- `app.py`: local Python HTTP server and enrollment logic.
- `school_clubs.db`, `schema.sql`, `seed.sql`, `search.sql`: database project files.
- `School_Clubs_Documentation.docx`: project documentation.
