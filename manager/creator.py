from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor


class Creator(ABC):

    @abstractmethod
    def create_one(self, info):
        pass

    def create_concurrently(self, infos, max_workers=20):
        """
                This method takes a list of information and creates entities concurrently
                using multiple threads.
                """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.create_one, info) for info in infos]
            results = [future.result() for future in futures]
        return results
