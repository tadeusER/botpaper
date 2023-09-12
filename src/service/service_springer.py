from typing import Union
import requests

from infrastructure.api_abstract import APIExtraction
from models.api_model import APIErrorResponse, APIResponse, APISuccessResponse
from models.paper_model import ArticleMetadata

class SpringerAPI(APIExtraction):
    """
    Clase que proporciona una interfaz para buscar artículos en Springer API.
    
    Atributos:
        BASE_URL (str): URL base para la API de Springer.
        
    Métodos:
        construct_query(): Construye una consulta basada en parámetros específicos.
        search(): Realiza una búsqueda en Springer API y devuelve los resultados.
        search_multiple_terms(): Realiza búsquedas múltiples en Springer API y agrega todos los resultados en una lista.
    """

    BASE_URL = "http://api.springernature.com/metadata/json"

    def __init__(self, api_key, default_results=10):
        """
        Inicializa una nueva instancia de la clase SpringerAPI.
        
        Args:
            api_key (str): La clave de API para Springer.
            default_results (int): El número predeterminado de resultados que se deben devolver por búsqueda.
        """
        self.api_key = api_key
        self.default_results = default_results

    def construct_query(self, term=None, title=None, orgname=None, journal=None, book=None, name=None):
        """
        Construye una consulta basada en parámetros específicos.

        Args:
            term (str): Término general para buscar.
            title (str): Título del artículo o capítulo.
            orgname (str): Nombre de la organización.
            journal (str): Título del journal.
            book (str): Título del libro.
            name (str): Nombre del autor.

        Returns:
            str: Una consulta construida para la API.
        """
        query_parts = []
        
        if term:
            query_parts.append(f'"{term}"')
        if title:
            query_parts.append(f'title:"{title}"')
        if orgname:
            query_parts.append(f'orgname:"{orgname}"')
        if journal:
            query_parts.append(f'journal:"{journal}"')
        if book:
            query_parts.append(f'book:"{book}"')
        if name:
            query_parts.append(f'name:"{name}"')

        return ' AND '.join(query_parts)

    def search(self, **kwargs)-> APIResponse:
        """
        Realiza una búsqueda en Springer API y devuelve los resultados.

        Args:
            **kwargs: Argumentos variables que se pasarán al constructor de consultas.

        Returns:
            APISuccessResponse: Respuesta con la lista de ArticleMetadata que coinciden con la consulta.
        """
        query = self.construct_query(**kwargs)

        params = {
            "q": query,
            "api_key": self.api_key,
            "p": self.default_results
        }

        response = requests.get(self.BASE_URL, params=params)
        records = response.json().get('records', [])
        articles = []

        for r in records:
            try:
                article = ArticleMetadata(
                    title=r['title'],
                    summary=r['abstract'],
                    published=r['publicationDate'],
                    link=r['doi']
                )
                articles.append(article)
            except Exception as e:
                print(f"Error al mapear el registro: {r}. Error: {e}")

        if articles:
            return APISuccessResponse(data=articles)
        else:
            return APIErrorResponse(error_message="No se pudo mapear ningún registro.")

    def search_multiple_terms(self, terms, **kwargs) -> Union[APISuccessResponse, APIErrorResponse]:
        all_results = []
        try:
            for term in terms:
                term_results = self.search(term=term, **kwargs)
                if isinstance(term_results, APISuccessResponse):
                    all_results.extend(term_results.data)
            return APISuccessResponse(data=all_results)
        except Exception as e:
            return APIErrorResponse(error_message=str(e))

if __name__ == "__main__":
    YOUR_API_KEY = "yourKeyHere"
    api = SpringerAPI(api_key=YOUR_API_KEY, default_results=10)
    
    # Ejemplo de búsqueda utilizando el nombre del autor y el título del artículo:
    search_results = api.search(name="Salvador", title="Quantum Computing")
    
    for paper in search_results:
        print(paper)
