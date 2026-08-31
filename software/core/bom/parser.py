import csv
from pathlib import Path
from typing import Union
from .models import BOMItem


class BOMParser:
    """Handles parsing and normalization of BOM CSV files."""

    @staticmethod
    def parse_csv(file_path: Union[str, Path]) -> list[BOMItem]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"BOM file not found: {path}")

        items: list[BOMItem] = []

        with open(path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            
            # Normalize headers (strip whitespace and convert to lowercase)
            if reader.fieldnames:
                reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

            for row_num, row in enumerate(reader, start=2):
                part_num = row.get("part_number", "").strip().upper()
                raw_qty = row.get("quantity_required", "").strip()
                raw_designators = row.get("designators", "").strip()
                description = row.get("description", "").strip() or None

                if not part_num:
                    continue  # Skip empty lines

                try:
                    qty = int(raw_qty)
                except ValueError:
                    raise ValueError(f"Row {row_num}: Invalid quantity '{raw_qty}' for part {part_num}")

                # Split designators by comma
                designators = [d.strip() for d in raw_designators.split(",") if d.strip()]

                items.append(
                    BOMItem(
                        part_number=part_num,
                        quantity_required=qty,
                        designators=designators,
                        description=description,
                    )
                )

        return items
