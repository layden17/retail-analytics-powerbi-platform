import pandas as pd
from sqlalchemy import create_engine, text

from src.config import DATABASE_URL, PROCESSED_DATA_DIR


def load_sales_to_postgres() -> None:
    """Charge sales_clean.parquet dans PostgreSQL."""

    input_path = PROCESSED_DATA_DIR / "sales_clean.parquet"

    print("Lecture du fichier Parquet...")
    sales = pd.read_parquet(input_path)

    print(f"Nombre de lignes à charger : {len(sales):,}")

    engine = create_engine(DATABASE_URL)

    print("Connexion à PostgreSQL...")
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Connexion réussie.")

    print("Chargement de la table staging_sales...")
    sales.to_sql(
        name="staging_sales",
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    print("Chargement terminé.")

    with engine.connect() as connection:
        row_count = connection.execute(
            text("SELECT COUNT(*) FROM public.staging_sales")
        ).scalar_one()

    print(f"Lignes présentes dans PostgreSQL : {row_count:,}")


if __name__ == "__main__":
    load_sales_to_postgres()