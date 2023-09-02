import requests

class SpringerAPI:
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

    def search(self, **kwargs):
        """
        Realiza una búsqueda en Springer API y devuelve los resultados.

        Args:
            **kwargs: Argumentos variables que se pasarán al constructor de consultas.

        Returns:
            list: Una lista de diccionarios que representan los artículos que coinciden con la consulta.
        """
        query = self.construct_query(**kwargs)

        params = {
            "q": query,
            "api_key": self.api_key,
            "p": self.default_results
        }

        response = requests.get(self.BASE_URL, params=params)
        return response.json().get('records', [])

    def search_multiple_terms(self, terms, **kwargs):
        """
        Realiza búsquedas múltiples en Springer API y agrega todos los resultados en una lista.

        Args:
            terms (list): Lista de términos a buscar.
            **kwargs: Argumentos variables que se pasarán al constructor de consultas.

        Returns:
            list: Una lista de diccionarios que representan los artículos que coinciden con las consultas.
        """
        all_results = []

        for term in terms:
            term_results = self.search(term=term, **kwargs)
            all_results.extend(term_results)

        return all_results

if __name__ == "__main__":
    YOUR_API_KEY = "yourKeyHere"
    api = SpringerAPI(api_key=YOUR_API_KEY, default_results=10)
    
    # Ejemplo de búsqueda utilizando el nombre del autor y el título del artículo:
    search_results = api.search(name="Salvador", title="Quantum Computing")
    
    for paper in search_results:
        print(paper)
