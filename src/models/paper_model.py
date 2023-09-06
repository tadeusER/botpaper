from datetime import datetime
from typing import Any

class ArticleMetadata:
    def __init__(self, title: str, summary: str, published: str, link: str):
        self.title = title
        self.summary = summary
        self.published = self._parse_date(published)
        self.link = link

    def _parse_date(self, date_str: str) -> datetime:
        """Convierte la fecha en string a un objeto datetime."""
        return datetime.fromisoformat(date_str)

    def __repr__(self) -> str:
        return (f"ArticleMetadata(title={self.title!r}, "
                f"summary={self.summary!r}, "
                f"published={self.published!r}, "
                f"link={self.link!r})")

    def to_dict(self) -> dict[str, Any]:
        """Convierte el objeto a un diccionario."""
        return {
            'title': self.title,
            'summary': self.summary,
            'published': self.published.isoformat(),
            'link': self.link
        }