import pandas as pd


def validate_sales_table(sales: pd.DataFrame) -> dict[str, int | bool]:
    """Contrôle la qualité de la table analytique sales."""

    duplicate_items = sales.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()

    missing_order_ids = sales["order_id"].isna().sum()
    missing_product_ids = sales["product_id"].isna().sum()
    negative_prices = sales["price"].lt(0).sum()
    negative_freight_values = sales["freight_value"].lt(0).sum()

    return {
        "rows": len(sales),
        "duplicate_items": int(duplicate_items),
        "missing_order_ids": int(missing_order_ids),
        "missing_product_ids": int(missing_product_ids),
        "negative_prices": int(negative_prices),
        "negative_freight_values": int(negative_freight_values),
        "item_key_is_unique": bool(duplicate_items == 0),
    }

def assert_sales_quality(sales: pd.DataFrame) -> None:
    """Arrête le pipeline si une règle critique n'est pas respectée."""

    results = validate_sales_table(sales)

    errors = []

    if results["duplicate_items"] > 0:
        errors.append(
            f"{results['duplicate_items']} doublons détectés sur la clé article."
        )

    if results["missing_order_ids"] > 0:
        errors.append(
            f"{results['missing_order_ids']} order_id manquants."
        )

    if results["missing_product_ids"] > 0:
        errors.append(
            f"{results['missing_product_ids']} product_id manquants."
        )

    if results["negative_prices"] > 0:
        errors.append(
            f"{results['negative_prices']} prix négatifs détectés."
        )

    if results["negative_freight_values"] > 0:
        errors.append(
            f"{results['negative_freight_values']} frais de livraison négatifs."
        )

    if errors:
        raise ValueError(
            "Validation de la table sales échouée :\n- "
            + "\n- ".join(errors)
        )