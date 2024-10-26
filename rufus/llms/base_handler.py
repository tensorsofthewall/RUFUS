from abc import ABC, abstractmethod

# Base class to abstract LLM instantiations
class LLMHandler(ABC):
    @abstractmethod
    def generate_text(self, prompt, **kwargs):
        """
        Generate text based on the provided prompt.
        """
        pass
    