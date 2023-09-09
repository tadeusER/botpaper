from typing import List, Dict, Type
from models.paper_model import ArticleMetadata
from models.api_model import APIResponse, APISuccessResponse
from service.service_arxiv import ArxivAPI
from service.service_cambrige import CambridgeAPI
from service.service_explorerieee import XploreAPI

class ResearchPaperSearcher:
    def __init__(self, tokens: Dict[str, str]):
        """
        Inicializa una nueva instancia de la clase ResearchPaperSearcher.

        Args:
            tokens (dict): Un diccionario que contiene tokens para los diferentes servicios.
        """
        self.tokens = tokens
        self.services = {
            "arxiv": ArxivAPI,
            "cambridge": CambridgeAPI,
            "xplore": XploreAPI,
        }

    def search(self, terms: List[str]) -> List[ArticleMetadata]:
        """
        Realiza una búsqueda en todos los servicios utilizando los términos proporcionados.

        Args:
            terms (list): Lista de términos a buscar.

        Returns:
            list: Lista de resultados obtenidos.
        """
        all_articles = []

        for service_name, service_class in self.services.items():
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
        all_articles = self.filter_articles(all_articles)
        return all_articles
    def filter_articles(self, articles: List[ArticleMetadata]) -> List[ArticleMetadata]:
        """
        Filtra una lista de artículos según una función de filtro específica.

        Args:
            articles (list): Lista de artículos a filtrar.
            filter_func (callable): Función de filtro que toma un ArticleMetadata y devuelve un booleano.

        Returns:
            list: Lista de artículos filtrados.
        """
        rest = self.sort_by_date(articles)
        return rest[:10]

    @staticmethod
    def sort_by_date(articles: List[ArticleMetadata]) -> List[ArticleMetadata]:
        """
        Ordena una lista de artículos por su fecha de publicación de forma descendente.

        Args:
            articles (list): Lista de artículos a ordenar.

        Returns:
            list: Lista de artículos ordenados por fecha.
        """
        return sorted(articles, key=lambda x: x.published, reverse=True)
