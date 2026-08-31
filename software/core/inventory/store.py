import csv
from pathlib import Path
from typing import Optional, Union
from .models import InventoryBin


class InventoryStore:
    """Manages physical bin stock allocations and lookups."""

    def __init__(self):
        self._bins: dict[str, InventoryBin] = {}  # bin_id -> InventoryBin
        self._part_map: dict[str, list[InventoryBin]] = {}  # part_number -> list[InventoryBin]

    def load_from_csv(self, file_path: Union[str, Path]) -> None:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Inventory file not found: {path}")

        with open(path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames:
                reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

            for row in reader:
                bin_id = row.get("bin_id", "").strip().upper()
                part_num = row.get("part_number", "").strip().upper()
                raw_qty = row.get("quantity_on_hand", "0").strip()
                unit = row.get("unit_of_measure", "PCS").strip()
                coord_x = int(row.get("coordinate_x", "0").strip())
                coord_y = int(row.get("coordinate_y", "0").strip())

                if not bin_id or not part_num:
                    continue

                bin_obj = InventoryBin(
                    bin_id=bin_id,
                    part_number=part_num,
                    quantity_on_hand=int(raw_qty),
                    unit_of_measure=unit,
                    coordinate_x=coord_x,
                    coordinate_y=coord_y,
                )

                self._bins[bin_id] = bin_obj
                self._part_map.setdefault(part_num, []).append(bin_obj)

    def find_bins_by_part(self, part_number: str) -> list[InventoryBin]:
        return self._part_map.get(part_number.strip().upper(), [])

    def get_bin(self, bin_id: str) -> Optional[InventoryBin]:
        return self._bins.get(bin_id.strip().upper())
