from sdks import XPLORE

class XploreAPI:
    def __init__(self, api_access_key, max_results=10):
        self.api_access_key = api_access_key
        self.max_results = max_results

    def construct_query(self, queries, search_types):
        query = XPLORE(self.api_access_key)
        
        for q, st in zip(queries, search_types):
            if st == "title":
                query.articleTitle(q)
            elif st == "author":
                query.authorText(q)
            elif st == "abstract":
                query.metaDataText(q)
            elif st == "year":
                query.publicationYear(q)

        return query

    def search(self, queries, search_types):
        constructed_query = self.construct_query(queries, search_types)
        data = constructed_query.callAPI()

        # Adapta la respuesta de Xplore a un formato similar al de ArxivAPI
        articles = []
        for entry in data["articles"]:  # Suponiendo que la respuesta tiene una clave 'articles'; cambia según la estructura real
            articles.append({
                "title": entry["title"],
                "summary": entry["abstract"],
                "published": entry["publication_date"],
                "link": entry["pdf_url"]
            })

        return articles

if __name__ == "__main__":
    api = XploreAPI('api_access_key', max_results=20)
    results = api.search(["Machine Learning", "Smith"], ["title", "author"])
    for paper in results:
        print(paper)
