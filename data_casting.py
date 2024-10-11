import re

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/lingvano", echo=True
)


def main():
    df = pd.read_sql("SELECT * from customer_transactions", engine)
    print(df.count())
    int_col = ["product_id", "customer_age_at_first_purchase", "quantity", "user_subscription_id"]
    str_col = [
        "order_status",
        "order_type",
        "product_name",
        "product_taxable_category",
        "customer_email",
        "customer_country",
        "customer_zip_code",
        "coupon_applied",
        "currency",
        "balance_currency",
        "source",
        "checkout",
    ]
    float_col = ["total", "tax", "fee", "balance_earnings"]

    df[str_col] = df[str_col].astype(str)
    df[int_col] = df[int_col].astype(int)
    df[float_col] = df[float_col].replace(",", "", regex=True).astype(float)
    df["date"] = pd.to_datetime(df["date"])
    df.to_sql("customer_transactions_cast", engine, index=False, if_exists="replace")


if __name__ == "__main__":
    main()
