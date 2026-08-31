from dataclasses import dataclass, field
from typing import Optional
from ..matching.engine import MatchedStep


@dataclass
class PickStep:
    """Represents a single executable pick action in the physical queue."""
    step_id: int
    bin_id: str
    part_number: str
    quantity: int
    coordinate_x: int
    coordinate_y: int
    status: str = "PENDING"  # PENDING -> ACTIVE -> CONFIRMED -> COMPLETED


class PickQueue:
    """Generates path-optimized pick sequences from matched BOM items."""

    @staticmethod
    def generate_sequence(matched_items: list[MatchedStep]) -> list[PickStep]:
        # Extract steps into raw list for sorting
        raw_steps = []
        for item in matched_items:
            raw_steps.append({
                "bin_id": item.target_bin.bin_id,
                "part_number": item.bom_item.part_number,
                "quantity": item.quantity_to_pick,
                "x": item.target_bin.coordinate_x,
                "y": item.target_bin.coordinate_y,
            })

        # Serpentine (S-Curve) Sort: Group by Y (row), then sort X based on row parity
        # Even rows: Left-to-Right (X ascending)
        # Odd rows: Right-to-Left (X descending)
        def serpentine_key(step):
            row = step["y"]
            col = step["x"] if row % 2 == 0 else -step["x"]
            return (row, col)

        sorted_steps = sorted(raw_steps, key=serpentine_key)

        # Build final PickStep objects with 1-based sequence IDs
        sequence: list[PickStep] = []
        for idx, step in enumerate(sorted_steps, start=1):
            sequence.append(
                PickStep(
                    step_id=idx,
                    bin_id=step["bin_id"],
                    part_number=step["part_number"],
                    quantity=step["quantity"],
                    coordinate_x=step["x"],
                    coordinate_y=step["y"],
                )
            )

        return sequence
