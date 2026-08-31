from dataclasses import dataclass


@dataclass
class InventoryBin:
    """Represents a physical storage bin and its component stock."""
    bin_id: str
    part_number: str
    quantity_on_hand: int
    unit_of_measure: str = "PCS"
    coordinate_x: int = 0
    coordinate_y: int = 0

    def __post_init__(self):
        if not self.bin_id or not self.bin_id.strip():
            raise ValueError("bin_id cannot be empty.")
        if self.quantity_on_hand < 0:
            raise ValueError(f"quantity_on_hand cannot be negative. Got: {self.quantity_on_hand}")
