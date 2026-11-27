from dataclasses import dataclass, asdict

@dataclass
class Article:
    id: int
    citation_key: str
    author: str
    title: str
    journal: str
    year: int
    type: str

    def to_dict(self) -> dict:
        return asdict(self)