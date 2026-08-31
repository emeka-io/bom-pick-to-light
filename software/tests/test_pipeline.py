from software.core.bom.models import BOMItem
from software.core.inventory.models import InventoryBin
from software.core.inventory.store import InventoryStore
from software.core.matching.engine import MatchingEngine
from software.core.pick_queue.queue import PickQueue


def test_matching_engine_and_pick_queue():
    store = InventoryStore()
    bin_1 = InventoryBin("BIN-A-01", "RES-10K-0805", 100, "PCS", 1, 1)
    bin_2 = InventoryBin("BIN-A-02", "CAP-100NF-0603", 50, "PCS", 2, 1)
    
    store._bins["BIN-A-01"] = bin_1
    store._part_map["RES-10K-0805"] = [bin_1]
    store._bins["BIN-A-02"] = bin_2
    store._part_map["CAP-100NF-0603"] = [bin_2]

    bom_items = [
        BOMItem("RES-10K-0805", 5, ["R1", "R2"]),
        BOMItem("CAP-100NF-0603", 2, ["C1"]),
    ]

    result = MatchingEngine.match(bom_items, store)
    assert result.is_executable is True
    assert len(result.matched_items) == 2

    sequence = PickQueue.generate_sequence(result.matched_items)
    assert len(sequence) == 2
    assert sequence[0].step_id == 1
    assert sequence[1].step_id == 2
