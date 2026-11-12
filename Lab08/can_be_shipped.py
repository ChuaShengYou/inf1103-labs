from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """Interface-style ABC: a contract for anything that can be shipped."""
    
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return a non-negative shipping charge."""