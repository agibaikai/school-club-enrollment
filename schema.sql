PRAGMA foreign_keys = ON;
CREATE TABLE students (
 student_id INTEGER PRIMARY KEY,
 full_name TEXT NOT NULL,
 class_group TEXT NOT NULL
);
CREATE TABLE clubs (
 club_id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 category TEXT NOT NULL,
 schedule TEXT NOT NULL,
 capacity INTEGER NOT NULL CHECK(capacity > 0)
);
CREATE TABLE enrollments (
 enrollment_id INTEGER PRIMARY KEY,
 student_id INTEGER NOT NULL REFERENCES students(student_id),
 club_id INTEGER NOT NULL REFERENCES clubs(club_id),
 enrolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(student_id, club_id)
);
