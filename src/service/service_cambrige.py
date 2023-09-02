import requests

class CambridgeAPI:
    """
    Clase que proporciona una interfaz para buscar artículos en el repositorio de Cambridge.

    Args:
        max_results (int): El número máximo de resultados que se deben devolver por búsqueda.

    Attributes:
        BASE_URL (str): La URL base para la API de Cambridge.

    Methods:
        search(): Realiza una búsqueda en el repositorio de Cambridge y devuelve una lista de artículos que coinciden con la consulta.
    """

    BASE_URL = "https://www.cambridge.org/engage/miir/public-api/v1/items"
    VALID_SORT_VALUES = [
        "VIEWS_COUNT_ASC", "VIEWS_COUNT_DESC", 
        "CITATION_COUNT_ASC", "CITATION_COUNT_DESC", 
        "READ_COUNT_ASC", "READ_COUNT_DESC", 
        "RELEVANT_ASC", "RELEVANT_DESC", 
        "PUBLISHED_DATE_ASC", "PUBLISHED_DATE_DESC"
    ]

    def __init__(self, max_results=10):
        """
        Inicializa una nueva instancia de la clase CambridgeAPI.

        Args:
            max_results (int): El número máximo de resultados que se deben devolver por búsqueda.
        """
        self.max_results = max_results

    def is_valid_sort_value(self, value):
        """
        Verifica si el valor proporcionado para 'sort' es válido.

        Args:
            value (str): El valor para verificar.

        Returns:
            bool: True si el valor es válido, False en caso contrario.
        """
        return value in self.VALID_SORT_VALUES

    def search(self, term="", skip=0, limit=None, sort="PUBLISHED_DATE_DESC", 
               author="", searchDateFrom="", searchDateTo="", categoryIds=None, subjectIds=None):
        """
        Realiza una búsqueda en el repositorio de Cambridge y devuelve una lista de artículos que coinciden con la consulta.

        Args:
            term (str): Término de búsqueda.
            skip (int): Cantidad de resultados a omitir.
            limit (int): Cantidad máxima de resultados a devolver.
            sort (str): Campo de ordenamiento.
            author (str): Autor específico a buscar.
            searchDateFrom (str): Fecha de inicio de búsqueda.
            searchDateTo (str): Fecha final de búsqueda.
            categoryIds (list): Lista de categorías.
            subjectIds (list): Lista de sujetos.

        Returns:
            list: Lista de resultados obtenidos.

        Raises:
            ValueError: Si se proporciona un tipo de ordenamiento no válido.
        """
        
        if not self.is_valid_sort_value(sort):
            raise ValueError(f"Invalid sort value provided. Got {sort}, expected one of {', '.join(self.VALID_SORT_VALUES)}")
        
        params = {
            "term": term,
            "skip": skip,
            "limit": limit or self.max_results,
            "sort": sort,
            "author": author,
            "searchDateFrom": searchDateFrom,
            "searchDateTo": searchDateTo
        }
        
        if categoryIds:
            params["categoryIds"] = categoryIds
        if subjectIds:
            params["subjectIds"] = subjectIds

        response = requests.get(self.BASE_URL, params=params)
        return response.json()
    def search_multiple_terms(self, terms):
        """
        Realiza búsquedas para cada término en la lista de términos y almacena todos los resultados en una lista.

        Args:
            terms (list): Lista de términos a buscar.

        Returns:
            list: Lista de todos los resultados obtenidos para cada término.
        """
        
        all_results = []

        for term in terms:
            term_results = self.search(term=term)
            all_results.extend(term_results)

        return all_results
if __name__ == "__main__":
    api = CambridgeAPI(max_results=20)
    results = api.search(term="IA", searchDateFrom="2020-01-01T00:00:00.000Z")
    for paper in results:
        print(paper)
    terms_to_search = ["IA", "Machine Learning", "Neural Networks"]
    all_search_results = api.search_multiple_terms(terms_to_search)
    
    for paper in all_search_results:
        print(paper)
