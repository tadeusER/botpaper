from datetime import datetime, timezone
from typing import Any, List

class ArticleMetadata:
    def __init__(self, title: str, summary: str, published: str, link: str):
        self.title = title
        self.summary = summary
        self.published = self._parse_date(published)
        self.link = link
    def _parse_date(self, date_str: str) -> datetime:
        """Convierte la fecha en string a un objeto datetime."""
        if date_str.endswith('Z'):
            date_str = date_str[:-1]  # quitar la 'Z'
            return datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
        else:
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

class Schedule:
    def __init__(self, 
                 channel: str, 
                 app: str, 
                 cron_schedule: str, 
                 search_keywords: List[str]) -> None:
        self.channel = channel
        self.app = app
        self.cron_schedule = cron_schedule
        self.search_keywords = search_keywords

    def __str__(self) -> str:
        return f"Channel: {self.channel}, App: {self.app}, Cron: {self.cron_schedule}, Keywords: {', '.join(self.search_keywords)}"

