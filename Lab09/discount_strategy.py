from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount turns an order total into a discounted total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Default strategy: the total is returned unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percent: float) -> None:
        if percent < 0 or percent > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percent: float = percent

    def get_percent(self) -> float:
        return self.__percent

    def apply(self, total: float) -> float:
        return total - total * self.__percent / 100


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)   # never return a negative total
        return total


class StudentDiscount(PercentageDiscount):
    """Fourth strategy (Section 2.4): a fixed 5% student discount.
    Added WITHOUT changing Order."""

    STUDENT_PERCENT = 5

    def __init__(self) -> None:
        super().__init__(self.STUDENT_PERCENT)
