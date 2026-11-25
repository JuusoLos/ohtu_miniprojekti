CREATE TABLE citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    citation_key TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    journal TEXT,
    year INTEGER NOT NULL,
    pages TEXT,
    publisher TEXT,
    edition TEXT,
    conference_name TEXT,
    city TEXT,
    type TEXT NOT NULL
);