from ibcs_mpl.data import from_records


def test_from_records_adapter() -> None:
    data = from_records(
        [{"m": "Jan", "v": 10}, {"m": "Feb", "v": 12}],
        category_key="m",
        value_key="v",
        name="Sales",
    )
    assert data.name == "Sales"
    assert list(data.categories) == ["Jan", "Feb"]
    assert list(data.values) == [10.0, 12.0]
