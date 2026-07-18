import pandas as pd
from pathlib import Path

def convert_order_dates(orders: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes de dates de la table orders."""

    orders = orders.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce",
        )

    return orders

def prepare_products(
    products: pd.DataFrame,
    category_translation: pd.DataFrame,
) -> pd.DataFrame:
    """Ajoute une catégorie produit exploitable en anglais."""

    products = products.copy()
    category_translation = category_translation.copy()

    products = products.merge(
        category_translation,
        on="product_category_name",
        how="left",
        validate="many_to_one",
    )

    products["product_category"] = (
        products["product_category_name_english"]
        .fillna(products["product_category_name"])
        .fillna("unknown")
    )

    return products

def prepare_payments(payments: pd.DataFrame) -> pd.DataFrame:
    """Agrège les paiements pour obtenir une ligne par commande."""

    payments = payments.copy()

    payment_summary = (
        payments.groupby("order_id", as_index=False)
        .agg(
            total_payment_value=("payment_value", "sum"),
            payment_count=("payment_sequential", "count"),
            payment_type_count=("payment_type", "nunique"),
            max_payment_installments=("payment_installments", "max"),
        )
    )

    main_payment_type = (
        payments.sort_values(
            ["order_id", "payment_value"],
            ascending=[True, False],
        )
        .drop_duplicates(subset="order_id")
        [["order_id", "payment_type"]]
        .rename(columns={"payment_type": "main_payment_type"})
    )

    payment_summary = payment_summary.merge(
        main_payment_type,
        on="order_id",
        how="left",
        validate="one_to_one",
    )

    return payment_summary

def prepare_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Agrège les avis pour obtenir une ligne par commande."""

    reviews = reviews.copy()

    date_columns = [
        "review_creation_date",
        "review_answer_timestamp",
    ]

    for column in date_columns:
        reviews[column] = pd.to_datetime(
            reviews[column],
            errors="coerce",
        )

    review_summary = (
        reviews.groupby("order_id", as_index=False)
        .agg(
            review_score=("review_score", "mean"),
            review_count=("review_id", "count"),
            has_review_comment=(
                "review_comment_message",
                lambda values: values.notna().any(),
            ),
            review_creation_date=("review_creation_date", "min"),
            review_answer_timestamp=("review_answer_timestamp", "max"),
        )
    )

    review_summary["customer_satisfaction"] = pd.cut(
        review_summary["review_score"],
        bins=[0, 2, 3, 5],
        labels=[
            "dissatisfied",
            "neutral",
            "satisfied",
        ],
    )

    return review_summary

def prepare_geolocation(
    geolocation: pd.DataFrame,
) -> pd.DataFrame:
    """Agrège la géolocalisation pour obtenir une ligne par code postal."""

    geolocation = geolocation.copy()

    geolocation_summary = (
        geolocation.groupby(
            "geolocation_zip_code_prefix",
            as_index=False,
        )
        .agg(
            latitude=("geolocation_lat", "mean"),
            longitude=("geolocation_lng", "mean"),
            city=("geolocation_city", "first"),
            state=("geolocation_state", "first"),
        )
    )

    return geolocation_summary

def build_sales_table(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    category_translation: pd.DataFrame,
    payments: pd.DataFrame,
    reviews: pd.DataFrame,
    sellers: pd.DataFrame,
    geolocation: pd.DataFrame,
) -> pd.DataFrame:
    """Construit la table analytique complète des ventes."""

    orders_clean = convert_order_dates(orders)

    products_clean = prepare_products(
        products,
        category_translation,
    )

    payments_clean = prepare_payments(payments)
    reviews_clean = prepare_reviews(reviews)
    geolocation_clean = prepare_geolocation(geolocation)

    sales = order_items.merge(
        orders_clean,
        on="order_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        products_clean[
            [
                "product_id",
                "product_category",
                "product_weight_g",
                "product_length_cm",
                "product_height_cm",
                "product_width_cm",
            ]
        ],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        payments_clean,
        on="order_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        reviews_clean,
        on="order_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        sellers,
        on="seller_id",
        how="left",
        validate="many_to_one",
    )

    customer_geolocation = geolocation_clean.rename(
        columns={
            "geolocation_zip_code_prefix": "customer_zip_code_prefix",
            "latitude": "customer_latitude",
            "longitude": "customer_longitude",
            "city": "customer_geo_city",
            "state": "customer_geo_state",
        }
    )

    seller_geolocation = geolocation_clean.rename(
        columns={
            "geolocation_zip_code_prefix": "seller_zip_code_prefix",
            "latitude": "seller_latitude",
            "longitude": "seller_longitude",
            "city": "seller_geo_city",
            "state": "seller_geo_state",
        }
    )

    sales = sales.merge(
        customer_geolocation,
        on="customer_zip_code_prefix",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        seller_geolocation,
        on="seller_zip_code_prefix",
        how="left",
        validate="many_to_one",
    )

    sales["product_revenue"] = sales["price"]

    sales["total_item_value"] = (
        sales["price"] + sales["freight_value"]
    )

    sales["delivery_time_days"] = (
        sales["order_delivered_customer_date"]
        - sales["order_purchase_timestamp"]
    ).dt.days

    sales["delivery_lateness_days"] = (
        sales["order_delivered_customer_date"]
        - sales["order_estimated_delivery_date"]
    ).dt.days

    sales["is_late_delivery"] = (
        sales["delivery_lateness_days"] > 0
    )

    sales["purchase_year"] = (
        sales["order_purchase_timestamp"].dt.year
    )

    sales["purchase_month"] = (
        sales["order_purchase_timestamp"].dt.month
    )

    sales["purchase_year_month"] = (
        sales["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype("string")
    )

    return sales


def save_processed_data(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """Enregistre un DataFrame nettoyé au format Parquet."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_parquet(
        output_path,
        index=False,
    )