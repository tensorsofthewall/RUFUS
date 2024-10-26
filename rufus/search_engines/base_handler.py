from abc import ABC, abstractmethod

# Base class to abstract search engine instantiations
class SearchEngineHandler(ABC):
    @abstractmethod
    def get_search_results(self, query, **kwargs):
        """
        Search the search engine for the given query.
        """
        pass