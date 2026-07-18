import pandas as pd

from src.cleaning import prepare_payments, prepare_products


def test_prepare_products_adds_final_category() -> None:
    products = pd.DataFrame(
        {
            "product_id": ["P1", "P2", "P3"],
            "product_category_name": [
                "beleza_saude",
                "informatica_acessorios",
                None,
            ],
        }
    )

    category_translation = pd.DataFrame(
        {
            "product_category_name": [
                "beleza_saude",
                "informatica_acessorios",
            ],
            "product_category_name_english": [
                "health_beauty",
                "computers_accessories",
            ],
        }
    )

    result = prepare_products(
        products,
        category_translation,
    )

    assert result.loc[0, "product_category"] == "health_beauty"
    assert result.loc[1, "product_category"] == "computers_accessories"
    assert result.loc[2, "product_category"] == "unknown"


def test_prepare_payments_returns_one_row_per_order() -> None:
    payments = pd.DataFrame(
        {
            "order_id": ["A", "A", "B"],
            "payment_sequential": [1, 2, 1],
            "payment_type": [
                "credit_card",
                "voucher",
                "debit_card",
            ],
            "payment_installments": [2, 1, 1],
            "payment_value": [80.0, 20.0, 50.0],
        }
    )

    result = prepare_payments(payments)

    assert result["order_id"].is_unique
    assert len(result) == 2

    order_a = result.loc[
        result["order_id"].eq("A")
    ].iloc[0]

    assert order_a["total_payment_value"] == 100.0
    assert order_a["payment_count"] == 2
    assert order_a["payment_type_count"] == 2
    assert order_a["max_payment_installments"] == 2
    assert order_a["main_payment_type"] == "credit_card"