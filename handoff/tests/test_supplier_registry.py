import json, os
P = os.path.join(os.path.dirname(__file__), "..", "supplier_qa_registry.json")


def test_printify_ornament_entry():
    e = json.load(open(P))["entries"][0]
    assert e["supplier"] == "Printify" and "ornament" in e["product"]
    assert e["max_shift_mm"] == 5 and e["symmetry_guaranteed"] is False
    assert "dashed" in e["safe_area"]


def test_every_entry_is_supplier_and_product_specific():
    for e in json.load(open(P))["entries"]:
        assert e["supplier"] and e["product"] and e["source"]
