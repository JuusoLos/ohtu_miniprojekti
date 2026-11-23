from dataclasses import dataclass

@dataclass
class Book:
    id: int
    citation_key: str
    author: str
    title: str
    year: int
    pages: str
    publisher: str
    type: str
