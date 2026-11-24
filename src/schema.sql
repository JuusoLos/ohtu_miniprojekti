CREATE TABLE "references" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    citation_key TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    journal TEXT,
    year INTEGER NOT NULL,
    pages TEXT,
    publisher TEXT,
    type TEXT NOT NULL
);