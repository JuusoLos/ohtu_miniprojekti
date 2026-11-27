from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: int
    citation_key: str
    author: str
    title: str
    year: int
    pages: str
    publisher: str
    edition: int 
    type: str

    def to_dict(self) -> dict:
        return asdict(self)