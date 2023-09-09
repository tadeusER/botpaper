from datetime import datetime, timezone
import re
from typing import Any, List

class ArticleMetadata:
    def __init__(self, title: str, summary: str, published: str, link: str):
        self.title = title
        self.summary = summary
        self.published = self._parse_date(published)
        self.link = link
    def clean_date_string(self, date_str: str) -> str:
        """Limpia la cadena de fecha eliminando caracteres no deseados y ajustando nombres de meses no estándar."""
        # Reemplaza nombres de meses no estándar
        month_replacements = {
            "Sept": "Sep"
        }
        for original, replacement in month_replacements.items():
            date_str = date_str.replace(original, replacement)
        
        # Elimina caracteres no deseados (no alfabéticos, numéricos, espacios, guiones o puntos)
        cleaned_str = re.sub(r"[^a-zA-Z0-9 .-]", "", date_str)
        # Asegura que haya un espacio entre el día y el mes y entre el mes y el año cuando hay puntos
        cleaned_str = re.sub(r"(\d)\.([A-Za-z])", r"\1 \2", cleaned_str)
        cleaned_str = re.sub(r"([A-Za-z])\.(\d)", r"\1 \2", cleaned_str)
        # Asegura que haya un espacio entre el día y el mes si no existe
        cleaned_str = re.sub(r"(\d)([A-Za-z])", r"\1 \2", cleaned_str)
        # Reemplaza múltiples espacios en blanco por un solo espacio
        cleaned_str = re.sub(r"\s+", " ", cleaned_str)
        # Limpia espacios al principio y al final
        return cleaned_str.strip()


    def _parse_date(self, date_str: str, cleaning_attempts: int = 0) -> datetime:
        """Convierte la fecha en string a un objeto datetime, manejando múltiples formatos."""
        if date_str.endswith('Z'):
            date_str = date_str[:-1]
            return datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)

        # Identifica patrones usando regex
        match_iso = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
        match_day_month_full_year = re.match(r"(\d{1,2}) ([A-Za-z]+) (\d{4})", date_str)
        match_day_month_year = re.match(r"(\d{1,2}) (\w+\.?) (\d{4})", date_str)
        match_range = re.match(r"(\d{1,2})-(\d{1,2}) (\w+\.?) (\d{4})", date_str)
        match_only_year = re.match(r"(\d{4})", date_str)
        match_month_year = re.match(r"([A-Za-z]+\.?) (\d{4})", date_str)

        if match_iso:
            return datetime.strptime(match_iso.group(1), "%Y-%m-%d")
        elif match_day_month_full_year:
            day, month, year = match_day_month_full_year.groups()
            if len(month) > 3:
                return datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
            else:
                return datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
        elif match_day_month_year:
            day, month, year = match_day_month_year.groups()
            if '.' in month:  # Si el mes tiene un punto
                return datetime.strptime(f"{day} {month[:-1]} {year}", "%d %b %Y")
            else:
                return datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
        elif match_range:
            # Solo usamos el primer día del rango, pero puedes ajustar esto según lo necesites.
            day, month, year = match_range.groups()[1:]
            if '.' in month:  # Si el mes tiene un punto
                return datetime.strptime(f"{day} {month[:-1]} {year}", "%d %b %Y")
            else:
                return datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
        elif match_only_year:
            year = match_only_year.group(1)
            return datetime.strptime(year, "%Y")
        elif match_month_year:
            month, year = match_month_year.groups()
            if '.' in month:
                return datetime.strptime(f"{month[:-1]} {year}", "%b %Y")
            else:
                return datetime.strptime(f"{month} {year}", "%B %Y")
        else:
            # Si todo falla y no hemos superado el límite de intentos de limpieza, intentamos limpiar la cadena y volver a parsearla
            if cleaning_attempts < 5:
                cleaned_str = self.clean_date_string(date_str)
                return self._parse_date(cleaned_str, cleaning_attempts + 1)
            else:
                raise ValueError(f"Couldn't parse the date string after multiple cleaning attempts: {date_str}")
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

