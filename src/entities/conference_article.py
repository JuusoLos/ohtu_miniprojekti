from dataclasses import dataclass, asdict

@dataclass
class ConferenceArticle:
    id: int
    citation_key: str
    author: str
    title: str
    year: int
    conference_name: str
    city: str
    type: str

    def to_dict(self) -> dict:
        return asdict(self)