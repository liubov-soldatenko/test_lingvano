import re

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


DATA_PATH = "./customer_transactions.csv"
CREATE_SQL = "./create_table.sql"
engine = create_engine('postgresql://postgres:postgres@localhost:5432/lingvano', echo=True)


def main():
    # Step 1 create table:
    with open(CREATE_SQL, 'r') as f:
        with engine.connect() as conn:
            conn.execute(text(f.read()))
    # Read data
    df = pd.read_csv(DATA_PATH)
    print(df.head())
    # Cleanup columns
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.map(lambda x: re.sub('\s+', '_', x.lower().strip()))
    df.columns = df.columns.map(lambda x: re.sub(r'[\(\)]', '', x.lower().strip()))
    print(df.columns)
    print(df.head())
    # load data to database
    df.to_sql('customer_transactions', engine, if_exists='append', index=False)


if __name__ == "__main__":
    main()
