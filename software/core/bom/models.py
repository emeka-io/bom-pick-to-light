from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class BOMItem:
    """Represents an individual line item parsed from a Bill of Materials."""
    part_number: str
    quantity_required: int
    designators: list[str] = field(default_factory=list)
    description: Optional[str] = None

    def __post_init__(self):
        if not self.part_number or not self.part_number.strip():
            raise ValueError("Part number cannot be empty.")
        if self.quantity_required <= 0:
            raise ValueError(f"Quantity required must be positive. Got: {self.quantity_required}")

