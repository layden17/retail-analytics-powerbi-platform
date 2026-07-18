import pandas as pd
import pytest

from src.validation import assert_sales_quality, validate_sales_table


def test_validate_sales_table_with_valid_data() -> None:
    sales = pd.DataFrame(
        {
            "order_id": ["A", "A", "B"],
            "order_item_id": [1, 2, 1],
            "product_id": ["P1", "P2", "P3"],
            "price": [10.0, 20.0, 15.0],
            "freight_value": [2.0, 3.0, 2.5],
        }
    )

    results = validate_sales_table(sales)

    assert results["duplicate_items"] == 0
    assert results["missing_order_ids"] == 0
    assert results["negative_prices"] == 0
    assert results["item_key_is_unique"] is True


def test_assert_sales_quality_with_duplicate_item() -> None:
    sales = pd.DataFrame(
        {
            "order_id": ["A", "A"],
            "order_item_id": [1, 1],
            "product_id": ["P1", "P1"],
            "price": [10.0, 10.0],
            "freight_value": [2.0, 2.0],
        }
    )

    with pytest.raises(ValueError, match="doublons"):
        assert_sales_quality(sales)


def test_assert_sales_quality_with_negative_price() -> None:
    sales = pd.DataFrame(
        {
            "order_id": ["A"],
            "order_item_id": [1],
            "product_id": ["P1"],
            "price": [-10.0],
            "freight_value": [2.0],
        }
    )

    with pytest.raises(ValueError, match="prix négatifs"):
        assert_sales_quality(sales)