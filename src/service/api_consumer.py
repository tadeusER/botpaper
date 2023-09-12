from datetime import timezone
import logging
from typing import List, Dict, Type, Optional
from models.paper_model import ArticleMetadata
from models.api_model import APIResponse, APISuccessResponse
from service.service_arxiv import ArxivAPI
from service.service_cambrige import CambridgeAPI
from service.service_explorerieee import XploreAPI
from service.service_springer import SpringerAPI

class ResearchPaperSearcher:
    def __init__(self, tokens: Dict[str, str], logger: Optional[logging.Logger] = None):
        """
        Inicializa una nueva instancia de la clase ResearchPaperSearcher.

        Args:
            tokens (dict): Un diccionario que contiene tokens para los diferentes servicios.
            logger (logging.Logger): Logger para registrar eventos y errores.
        """
        self.tokens = tokens
        self.services = {
            "arxiv": ArxivAPI,
            "cambridge": CambridgeAPI,
            "xplore": XploreAPI,
            "springer": SpringerAPI
        }
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("ResearchPaperSearcher initialized.")

    def search(self, terms: List[str]) -> List[ArticleMetadata]:
        self.logger.info(f"Starting search for terms: {terms}")
        all_articles = []

        for service_name, service_class in self.services.items():
            try:
                if service_name in self.tokens:
                    api = service_class(api_access_key=self.tokens[service_name])
                    response = api.search_multiple_terms(terms)
                    if isinstance(response, APISuccessResponse):
                        all_articles.extend(response.data)
                else:
                    api = service_class()
                    response = api.search_multiple_terms(terms)
                    if isinstance(response, APISuccessResponse):
                        all_articles.extend(response.data)
                self.logger.info(f"Found {len(response.data)} articles in {service_name}.")
            except Exception as e:
                self.logger.error(f"Error searching in {service_name}: {str(e)}")

        all_articles = self.filter_articles(all_articles)
        self.logger.info(f"Search completed. Found {len(all_articles)} articles.")
        return all_articles

    def filter_unique_articles(self, articles: List[ArticleMetadata]) -> List[ArticleMetadata]:
        self.logger.info("Filtering unique articles...")
        seen_titles = set()
        seen_links = set()
        unique_articles = []

        for article in articles:
            if article.title not in seen_titles and article.link not in seen_links:
                seen_titles.add(article.title)
                seen_links.add(article.link)
                unique_articles.append(article)

        self.logger.info(f"Filtered {len(articles) - len(unique_articles)} duplicate articles.")
        return unique_articles

    def filter_articles(self, articles: List[ArticleMetadata]) -> List[ArticleMetadata]:
        try:
            if not articles:
                self.logger.warning("The article list is empty. No articles to filter.")
                return []

            self.logger.info("Applying article filters...")
            filtered = self.filter_unique_articles(articles)
            rest = self.sort_by_date(filtered)
            return rest[:10]
        except Exception as e:
            self.logger.error(f"An error occurred while filtering articles: {e}")
            return []
        
    def sort_by_date(self, articles: List[ArticleMetadata]) -> List[ArticleMetadata]:
        try:
            if not all(hasattr(article, 'published') for article in articles):
                raise ValueError("Some articles don't have a 'published' attribute.")
            # Asegurar que todos los objetos datetime tengan zona horaria
            for article in articles:
                if article.published.tzinfo is None:
                    article.published = article.published.replace(tzinfo=timezone.utc)
                    
            return sorted(articles, key=lambda x: x.published, reverse=True)
        except Exception as e:
            self.logger.error(f"An error occurred while sorting articles by date: {e}")
            return articles 

