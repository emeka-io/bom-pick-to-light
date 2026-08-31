# Test Plan — BOM Pick-to-Light System

## 1. Overview
This test plan defines the testing architecture and validation criteria across the software core, matching algorithms, sequence engine, and hardware communication layer.

---

## 2. Test Architecture & Tooling

* **Test Framework:** `pytest` (Python 3.10+)
* **Coverage Targets:** >= 90% core coverage across parsing, inventory, and matching logic
* **Mocking:** `unittest.mock` for simulating physical serial hardware interfaces

---

## 3. Test Suites & Verification Criteria

| Test Suite | File Location | Scope / Objectives | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **BOM Parsing** | `software/tests/test_parser.py` | CSV/JSON ingestion, header extraction, designator splitting | Valid `BOMItem` objects generated; malformed files raise exceptions |
| **Inventory Store** | `software/tests/test_inventory.py` | Stock lookups, quantity updates, deficit detection | Correct stock levels maintained post-pick; deficits flagged |
| **Matching Engine** | `software/tests/test_matching.py` | MPN string normalization, cross-referencing BOM items | Clean separation of `matched_items`, `unmapped_items`, and `deficit_items` |
| **Pick Queue** | `software/tests/test_queue.py` | Serpentine coordinate sorting, path optimization | Pick steps ordered to minimize operator path travel |
| **Serial Comms** | `software/tests/test_comms.py` | Packet serialization, frame checksums, mock ACK handling | Valid byte payloads emitted; timeouts handled gracefully |

---

## 4. Test Execution Commands

Run unit tests locally in the terminal:

```bash
# Run full unit test suite
pytest software/tests/

# Run with coverage report
pytest --cov=software/core software/tests/
```
