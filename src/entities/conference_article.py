from dataclasses import dataclass

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
