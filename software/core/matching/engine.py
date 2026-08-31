from dataclasses import dataclass, field
from typing import Optional
from ..bom.models import BOMItem
from ..inventory.models import InventoryBin
from ..inventory.store import InventoryStore


@dataclass
class MatchedStep:
    """Represents a successfully mapped pick step."""
    bom_item: BOMItem
    target_bin: InventoryBin
    quantity_to_pick: int


@dataclass
class StockDeficit:
    """Represents a component with insufficient stock in inventory."""
    part_number: str
    quantity_required: int
    quantity_available: int


@dataclass
class MatchResult:
    """Container for the complete BOM reconciliation outcome."""
    matched_items: list[MatchedStep] = field(default_factory=list)
    unmapped_items: list[BOMItem] = field(default_factory=list)
    deficit_items: list[StockDeficit] = field(default_factory=list)

    @property
    def is_executable(self) -> bool:
        """Returns True if every BOM item is mapped with sufficient stock."""
        return len(self.unmapped_items) == 0 and len(self.deficit_items) == 0


class MatchingEngine:
    """Reconciles BOM requests against physical inventory bins."""

    @staticmethod
    def match(bom_items: list[BOMItem], inventory_store: InventoryStore) -> MatchResult:
        result = MatchResult()

        for item in bom_items:
            bins = inventory_store.find_bins_by_part(item.part_number)

            if not bins:
                result.unmapped_items.append(item)
                continue

            # Calculate total available stock across all matching bins
            total_available = sum(b.quantity_on_hand for b in bins)

            if total_available < item.quantity_required:
                result.deficit_items.append(
                    StockDeficit(
                        part_number=item.part_number,
                        quantity_required=item.quantity_required,
                        quantity_available=total_available,
                    )
                )
            else:
                # Assign to primary bin (first bin with adequate stock)
                primary_bin = bins[0]
                result.matched_items.append(
                    MatchedStep(
                        bom_item=item,
                        target_bin=primary_bin,
                        quantity_to_pick=item.quantity_required,
                    )
                )

        return result
