import pandas as pd

# Load raw dataset
df = pd.read_csv("data/online_retail.csv", encoding="ISO-8859-1")

print("Initial shape:", df.shape)

# Rename columns for consistency
df.columns = [
    "invoice_no", "stock_code", "description", "quantity",
    "invoice_date", "unit_price", "customer_id", "country"
]

# Convert data types
df["invoice_date"] = pd.to_datetime(df["invoice_date"])

# Remove cancelled invoices
df = df[~df["invoice_no"].astype(str).str.startswith("C")]

# Remove returns and invalid quantities
df = df[df["quantity"] > 0]

# Remove missing customer IDs (needed for customer analytics)
df = df.dropna(subset=["customer_id"])

# Feature engineering
df["revenue"] = df["quantity"] * df["unit_price"]
df["order_month"] = df["invoice_date"].dt.to_period("M").astype(str)

# Save cleaned data
df.to_csv("data/clean_ecommerce.csv", index=False)

print("Cleaned shape:", df.shape)
print("✅ clean_ecommerce.csv created")
