import pytest
from software.core.bom.parser import BOMParser


def test_parse_valid_csv(tmp_path):
    csv_file = tmp_path / "valid_bom.csv"
    csv_file.write_text(
        "part_number,quantity_required,designators,description\n"
        'RES-10K-0805,4,"R1, R2, R3, R4",10k Resistor\n'
    )

    items = BOMParser.parse_csv(csv_file)
    assert len(items) == 1
    assert items[0].part_number == "RES-10K-0805"
    assert items[0].quantity_required == 4
    assert items[0].designators == ["R1", "R2", "R3", "R4"]


def test_parse_missing_file():
    with pytest.raises(FileNotFoundError):
        BOMParser.parse_csv("non_existent_file.csv")


def test_parse_invalid_quantity(tmp_path):
    csv_file = tmp_path / "bad_qty.csv"
    csv_file.write_text(
        "part_number,quantity_required\n"
        "RES-10K-0805,INVALID_QTY\n"
    )

    with pytest.raises(ValueError, match="Invalid quantity"):
        BOMParser.parse_csv(csv_file)
