from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass(frozen=True)
class Orderline:
    orderid: str
    sku: str
    qty: int


class Batch:
    
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.purchased_quantity = qty
        self._allocations = set() #

    def allocate(self, line: Orderline):
        if self.can_allocate(line):
            self._allocations.remove(line)
    
    def deallocate(self, line: Orderline):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)


    def can_allocate(self, line:Orderline) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty