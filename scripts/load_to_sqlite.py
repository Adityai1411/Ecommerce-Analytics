import pandas as pd
import sqlite3

# Load cleaned data
df = pd.read_csv("data/clean_ecommerce.csv")

# Connect to SQLite DB
conn = sqlite3.connect("ecommerce.db")

# Load data into table
df.to_sql("sales", conn, if_exists="replace", index=False)

conn.close()

print("✅ clean_ecommerce loaded into ecommerce.db (table: sales)")
