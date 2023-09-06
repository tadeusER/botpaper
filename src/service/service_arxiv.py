import urllib.parse
import urllib.request
import feedparser
from infrastructure.api_abstract import APIExtraction
from models.api_model import APIResponse, APISuccessResponse, APIErrorResponse

class ArxivAPI(APIExtraction):

    BASE_URL = ("http://export.arxiv.org/api/query?"
                "search_query={}&sortBy=lastUpdatedDate&sortOrder=ascending&max_results={}")
    valid_search_types = ["ti", "au", "abs", "co", "jr", "cat", "rn", "id", "all"]

    def __init__(self, max_results=10):
        self.max_results = max_results

    def is_valid_search_type(self, search_type):
        return search_type in self.valid_search_types

    def construct_query(self, queries, search_types, operators):
        if not all([self.is_valid_search_type(st) for st in search_types]):
            raise ValueError("Invalid search type provided.")
        queries = [q.lower() for q in queries]
        search_types = [st.lower() for st in search_types]
        combined_queries = []
        for i, (query, search_type) in enumerate(zip(queries, search_types)):
            combined_query = "{}:{}".format(search_type, query)
            combined_queries.append(combined_query)
            if i < len(queries) - 1:
                combined_queries.append(operators[i])
        return '+'.join(combined_queries)

    def search(self, queries, search_types, operators=None) -> APIResponse:
        if operators is None:
            operators = ["AND"] * (len(queries) - 1)
        try:
            constructed_query = self.construct_query(queries, search_types, operators)
            url = self.BASE_URL.format(constructed_query, self.max_results)
            response = urllib.request.urlopen(url)
            feed = feedparser.parse(response.read().decode('utf-8'))
            articles = []
            for entry in feed.entries:
                articles.append({
                    "title": entry.title,
                    "summary": entry.summary,
                    "published": entry.published,
                    "link": entry.link
                })
            return APISuccessResponse(data=articles)
        except Exception as e:
            return APIErrorResponse(error_message=str(e))

    def search_multiple_terms(self, terms) -> APIResponse:
        combined_articles = []
        for term in terms:
            response = self.search([term], ["all"])
            if isinstance(response, APISuccessResponse):
                combined_articles.extend(response.data)
        if combined_articles:
            return APISuccessResponse(data=combined_articles)
        else:
            return APIErrorResponse(error_message="No results found for any term.")

    def is_valid_sort_value(self, value) -> bool:
        # Implementar según la lógica requerida para arXiv si es necesario.
        pass

if __name__ == "__main__":
    api = ArxivAPI(max_results=20)
    results_combined = api.search(["Rovs", "AUV"], ["all", "all"], ["OR"])
    if isinstance(results_combined, APISuccessResponse):
        for paper in results_combined.data:
            print(paper)
    else:
        print(f"Error: {results_combined.error_message}")