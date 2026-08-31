import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from software.core.bom.parser import BOMParser
from software.core.inventory.store import InventoryStore
from software.core.matching.engine import MatchingEngine
from software.core.pick_queue.queue import PickQueue
from software.core.comms.serial_driver import SerialDriver


def run_pipeline(bom_path: str, inventory_path: str) -> None:
    print("==================================================")
    print("   BOM PICK-TO-LIGHT SYSTEM ENGINE EXECUTION      ")
    print("==================================================\n")

    # 1. Ingest BOM
    print(f"[*] Ingesting BOM dataset from: {bom_path}")
    bom_items = BOMParser.parse_csv(bom_path)
    print(f"[+] Loaded {len(bom_items)} BOM line items.\n")

    # 2. Load Inventory Store
    print(f"[*] Ingesting Inventory Store dataset from: {inventory_path}")
    store = InventoryStore()
    store.load_from_csv(inventory_path)
    print(f"[+] Inventory loaded successfully.\n")

    # 3. Match and Reconcile
    print("[*] Reconciling BOM items against physical bin store...")
    match_result = MatchingEngine.match(bom_items, store)

    if not match_result.is_executable:
        print("\n[!] ERROR: Reconciliation failed. Job cannot be executed.")
        if match_result.unmapped_items:
            print(f"    - Unmapped Parts: {len(match_result.unmapped_items)}")
        if match_result.deficit_items:
            print(f"    - Stock Deficits: {len(match_result.deficit_items)}")
        sys.exit(1)

    print("[+] Reconciliation SUCCESS: All BOM items matched with sufficient stock.\n")

    # 4. Generate Pick Queue
    print("[*] Generating S-Curve path-optimized pick sequence...")
    sequence = PickQueue.generate_sequence(match_result.matched_items)
    print(f"[+] Sequence generated with {len(sequence)} pick steps:\n")

    for step in sequence:
        print(f"  [Step {step.step_id}] Bin: {step.bin_id:<10} | Part: {step.part_number:<18} | Qty: {step.quantity} | Grid: ({step.coordinate_x}, {step.coordinate_y})")

    # 5. Simulate Serial Framing
    print("\n[*] Initializing Serial Driver interface...")
    driver = SerialDriver(port="COM3")
    driver.connect()

    print("[*] Dispatching hardware LED pick commands:")
    for step in sequence:
        packet = driver.send_pick_command(bin_id=step.bin_id, color_hex="00FF00", qty=step.quantity)
        print(f"  -> TX: {packet}")

    driver.disconnect()
    print("\n[+] Pick-to-Light execution sequence dispatched successfully.")


if __name__ == "__main__":
    default_bom = "data/example-boms/example-bom.csv"
    default_inv = "data/example-inventory/example-inventory.csv"
    run_pipeline(default_bom, default_inv)
