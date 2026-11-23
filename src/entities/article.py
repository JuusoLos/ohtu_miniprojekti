from dataclasses import dataclass

@dataclass
class Article:
    id: int
    citation_key: str
    author: str
    title: str
    journal: str
    year: int
    type: str