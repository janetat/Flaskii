DROP table if EXISTS entries;
CREATE table entries (
  id INTEGER PRIMARY KEY autoincrement,
  title TEXT NOT NULL,
  text TEXT NOT NULL
);