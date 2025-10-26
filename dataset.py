import pandas as pd

# Load the CSV file
df = pd.read_csv("data/brasil_real-estate-1.csv")

# Validate shape
assert df.shape == (12834, 6), "Dataset must have 12,834 rows and 6 columns"

# Apply formatting rules
df['property_type'] = df['property_type'].str.lower()

df['place_with_parent_names'] = df['place_with_parent_names'].apply(
    lambda x: f"|{x.strip().replace(', ', '|')}|"
)

# Convert price_usd to numeric first (handle errors gracefully)
df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')

# Format price_usd with $ and commas
df['price_usd'] = df['price_usd'].apply(
    lambda x: f"${x:,.2f}" if pd.notnull(x) else None
)

# Save the transformed data to a new CSV file
df.to_csv("brasil_real_estate_transformed.csv", index=False)

print("✅ Transformed CSV saved as 'brasil_real_estate_transformed.csv'")
