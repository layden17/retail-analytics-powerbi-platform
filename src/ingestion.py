import pandas as pd

from src.cleaning import (
    build_sales_table,
    save_processed_data,
)
from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from src.validation import assert_sales_quality


def load_raw_data() -> dict[str, pd.DataFrame]:
    """Charge les fichiers CSV bruts du projet."""

    return {
        "orders": pd.read_csv(
            RAW_DATA_DIR / "olist_orders_dataset.csv"
        ),
        "order_items": pd.read_csv(
            RAW_DATA_DIR / "olist_order_items_dataset.csv"
        ),
        "customers": pd.read_csv(
            RAW_DATA_DIR / "olist_customers_dataset.csv"
        ),
        "products": pd.read_csv(
            RAW_DATA_DIR / "olist_products_dataset.csv"
        ),
        "category_translation": pd.read_csv(
            RAW_DATA_DIR / "product_category_name_translation.csv"
        ),
        "payments": pd.read_csv(
            RAW_DATA_DIR / "olist_order_payments_dataset.csv"
        ),
        "reviews": pd.read_csv(
            RAW_DATA_DIR / "olist_order_reviews_dataset.csv"
        ),
        "sellers": pd.read_csv(
            RAW_DATA_DIR / "olist_sellers_dataset.csv"
        ),
        "geolocation": pd.read_csv(
            RAW_DATA_DIR / "olist_geolocation_dataset.csv"
        ),
    }


def run_pipeline() -> None:
    """Exécute le pipeline de préparation des données."""

    print("Chargement des données brutes...")
    raw_data = load_raw_data()

    print("Construction de la table analytique...")
    sales_clean = build_sales_table(
        orders=raw_data["orders"],
        order_items=raw_data["order_items"],
        customers=raw_data["customers"],
        products=raw_data["products"],
        category_translation=raw_data["category_translation"],
        payments=raw_data["payments"],
        reviews=raw_data["reviews"],
        sellers=raw_data["sellers"],
        geolocation=raw_data["geolocation"],
    )

    print("Validation de la qualité...")
    assert_sales_quality(sales_clean)

    output_path = (
        PROCESSED_DATA_DIR
        / "sales_clean.parquet"
    )

    print("Enregistrement des données...")
    save_processed_data(
        dataframe=sales_clean,
        output_path=output_path,
    )

    print(f"Pipeline terminé : {output_path}")
    print(f"Nombre de lignes : {len(sales_clean):,}")


if __name__ == "__main__":
    run_pipeline()