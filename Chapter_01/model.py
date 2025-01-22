from dataclasses import dataclass
from typing import Optional
from datetime import date
from typing import NewType
from typing import NamedTuple
from collections import namedtuple

Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Money(NamedTuple):
    currency: str
    value: int

Line = namedtuple('Line', ['sku', 'qty'])

@dataclass(frozen=True)
class Orderline:
    orderid: str
    sku: str
    qty: int


class Batch:
    
    def __init__(self, ref: Reference, sku: Sku, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
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

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self._allocations

    def can_allocate(self, line:Orderline) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty