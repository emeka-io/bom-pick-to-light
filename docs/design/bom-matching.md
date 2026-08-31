# Design Specification — BOM Matching Strategy & Engine Logic

## 1. Overview
The BOM Matching Engine bridges ingested design files (BOMs) with the physical inventory database (`InventoryStore`). It normalizes part numbers, validates stock availability, resolves designator groups, and flags any unmapped or understocked items before sequence generation.

---

## 2. Ingestion & Part Number Normalization Rules

Raw BOM exports from EDA/CAD tools contain variations in whitespace, case, and formatting. The matching engine applies string normalization prior to lookup:

1. **Case Standardizing:** Convert all characters to upper case (`res-10k-0805` -> `RES-10K-0805`).
2. **Whitespace Trimming:** Strip leading, trailing, and redundant spaces.
3. **Delimiter Cleaning:** Standardize dash/underscore separators.
4. **Designator Parsing:** Expand aggregated designator strings (e.g., `"C1, C2, C3"` -> `["C1", "C2", "C3"]`, `quantity_required = 3`).

---

## 3. Matching Algorithm & State Decision Tree

For each normalized line item in the BOM, the matching engine executes the following evaluation flow:

```text
               +-----------------------------+
               | Ingest Normalized BOM Item  |
               +-----------------------------+
                              |
                              v
                /---------------------------\
               /   Exact MPN Match Found     \
               \   in InventoryStore?        /
                \---------------------------/
                  /                       \
               YES                         NO
               /                             \
              v                               v
    /-------------------\           +-------------------+
   / Stock >= Quantity   \          | Status: UNMAPPED  |
   \    Required?        /          | Log missing part  |
    \-------------------/           +-------------------+
      /               \                       |
    YES                NO                     v
    /                    \            [ Halt / User Flag ]
   v                      v
+------------------+  +----------------------+
| Status: MATCHED  |  | Status: DEFICIT      |
| Reserve required |  | Flag available vs    |
| units            |  | required shortfall   |
+------------------+  +----------------------+

```
## 4. Output Reconciliation Report Schema
Upon execution, the engine produces a MatchResult data structure:

Field,Type,Description
matched_items,list[MatchedStep],Validated BOM line items paired with physical bin_id locations
unmapped_items,list[BOMItem],BOM items missing corresponding entries in the inventory store
deficit_items,list[StockDeficit],Items found in inventory but lacking sufficient quantity_on_hand
is_executable,Boolean,Returns True only if unmapped_items and deficit_items are empty


## 5. Sample Python Execution Example
```python
@dataclass
class MatchResult:
    matched_items: list[dict]
    unmapped_items: list[dict]
    deficit_items: list[dict]

    @property
    def is_executable(self) -> bool:
        return len(self.unmapped_items) == 0 and len(self.deficit_items) == 0

```


