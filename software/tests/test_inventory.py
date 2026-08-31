import pytest
from software.core.inventory.store import InventoryStore


def test_inventory_store_load_and_query(tmp_path):
    inv_file = tmp_path / "inventory.csv"
    inv_file.write_text(
        "bin_id,part_number,quantity_on_hand,unit_of_measure,coordinate_x,coordinate_y\n"
        "BIN-A-01,RES-10K-0805,150,PCS,1,1\n"
    )

    store = InventoryStore()
    store.load_from_csv(inv_file)

    bins = store.find_bins_by_part("RES-10K-0805")
    assert len(bins) == 1
    assert bins[0].bin_id == "BIN-A-01"
    assert bins[0].quantity_on_hand == 150


def test_inventory_missing_file():
    store = InventoryStore()
    with pytest.raises(FileNotFoundError):
        store.load_from_csv("missing_inventory.csv")
