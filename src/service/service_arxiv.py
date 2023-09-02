import urllib.parse
import urllib.request
import feedparser

class ArxivAPI:
    
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

        # Convert queries and search_types to lowercase.
        queries = [q.lower() for q in queries]
        search_types = [st.lower() for st in search_types]

        combined_queries = []
        for i, (query, search_type) in enumerate(zip(queries, search_types)):
            combined_query = "{}:{}".format(search_type, query)
            combined_queries.append(combined_query)

            if i < len(queries) - 1:
                combined_queries.append(operators[i])
        
        return '+'.join(combined_queries)

    def search(self, queries, search_types, operators=None):
        if operators is None:
            operators = ["AND"] * (len(queries) - 1)
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
        
        return articles

if __name__ == "__main__":
    api = ArxivAPI(max_results=20)

    # Example of combining author and title search
    results_combined = api.search(["Rovs", "AUV"], ["all", "all"], ["OR"])
    for paper in results_combined:
        print(paper)
