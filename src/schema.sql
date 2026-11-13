CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    citation_key TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    journal TEXT NOT NULL,
    year INTEGER NOT NULL
);