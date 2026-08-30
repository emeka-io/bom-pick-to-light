### Software Architecture — BOM Pick-to-Light System

## 1. Module Structure

The host software is implemented as a modular Python package located inside `software/core/`:

```text
software/core/
├── bom/
│   ├── parser.py           # Ingests and standardizes raw CSV/JSON BOMs
│   └── models.py           # Dataclasses for BOM items and quantities
├── inventory/
│   ├── store.py            # Manages bin allocations and stock levels
│   └── models.py           # Dataclasses for Bin, Part, and Location
├── matching/
│   └── engine.py           # Reconciles BOM requests against InventoryStore
├── pick_queue/
│   └── queue.py            # Generates coordinate-sorted pick sequences
└── comms/
    └── serial_driver.py    # Manages host-to-MCU serial protocol framing

```

## 2. Core Data Models
# 2.1 BOM Item Model

```python
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BOMItem:
    part_number: str
    quantity_required: int
    designators: list[str]
    description: Optional[str] = None

```

# 2.2 Inventory Bin Model

```python
from dataclasses import dataclass

@dataclass
class InventoryBin:
    bin_id: str  # e.g., "BIN-A-01"
    part_number: str
    quantity_on_hand: int
    coordinate_x: int  # Physical grid column
    coordinate_y: int  # Physical grid row
```

## 3. Class Interactions & Responsibilities

| Class | Responsibilities | Inputs | Outputs |
| :--- | :--- | :--- | :--- |
| **BOMParser** | Validates file structure, strips whitespace, parses quantities | Raw CSV / JSON path | `list[BOMItem]` |
| **InventoryStore** | Tracks bin stock, updates inventory post-pick | Query requests | `InventoryBin` or `StockDeficit` |
| **MatchingEngine** | Cross-references `BOMItem` with `InventoryBin` | `list[BOMItem]`, `InventoryStore` | `MatchResult` (Matches & Unmapped list) |
| **PickQueue** | Orders items by path distance to optimize retrieval time | `MatchResult` | Ordered `list[PickStep]` |
| **SerialDriver** | Serializes command packets (`SET_LED`, `RESET_ALL`) | `PickStep` | Byte stream over Serial / UART |


4. Error Handling & Edge Cases
- Unmapped Part Exception: Raised when a BOM item does not map to any existing bin_id. The engine logs the failure and halts sequence generation.

- Insufficient Stock Exception: Raised when quantity_required > quantity_on_hand. Generates a warning flag allowing partial picking or job abort.

- Serial Timeout Exception: Triggered if MCU fails to return ACK within 5 seconds of packet transmission. Host enters retry loop (max 3 attempts).