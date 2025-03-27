import pandas as pd

# Read CSV files
df_houses = pd.read_csv("london_houses.csv")
df_prices = pd.read_csv("London.csv")

# View sample data
print("📌 Sample house price data:")
print(df_prices.head())

print("\n📌 Sample housing characteristics data:")
print(df_houses.head())

# Check for missing values
print("\n📌 Missing value statistics:")
print(df_prices.isnull().sum())
print(df_houses.isnull().sum())

# View unique values of Location
print(df_prices["Location"].unique())

# View unique Neighborhood values
print("📌 Unique values in `Neighborhood` from 'london_houses.csv':")
print(df_houses["Neighborhood"].unique())

# View unique Location values
print("\n📌 Unique values in `Location` from 'London.csv':")
print(df_prices["Location"].unique())

# Create mapping from Neighborhood to Borough (Location)
neighborhood_to_location = {
    "Notting Hill": "Kensington and Chelsea",
    "Soho": "Westminster",
    "Marylebone": "Westminster",
    "Camden": "Camden",
    "Shoreditch": "Hackney",
    "Greenwich": "Greenwich",
    "Kensington": "Kensington and Chelsea",
    "Chelsea": "Kensington and Chelsea",
    "Islington": "Islington",
    "Westminster": "Westminster",
    "Wimbledon": "Merton",
    "Putney": "Wandsworth",
    "Clerkenwell": "Islington",
    "Fulham": "Hammersmith and Fulham",
    "Highgate": "Camden",
    "Battersea": "Wandsworth",
    "Hampstead": "Camden",
    "Tooting": "Wandsworth",
    "Canary Wharf": "Tower Hamlets",
    "Ealing": "Ealing",
    "Hackney": "Hackney",
    "Whitechapel": "Tower Hamlets",
    "Mayfair": "Westminster",
    "Fitzrovia": "Camden",
    "Pimlico": "Westminster",
    "South Bank": "Lambeth",
}

# Map Neighborhood to standardized Location
df_houses["Mapped_location"] = df_houses["Neighborhood"].map(neighborhood_to_location)

# Check unmatched Neighborhoods
unmatched = df_houses[df_houses["Mapped_location"].isnull()]["Neighborhood"].unique()
print("❌ The following `Neighborhood` values could not be matched to any `Location`:")
print(unmatched)

# Merge the two datasets
df_merged = pd.merge(df_houses, df_prices, left_on="Neighborhood", right_on="Location", how="left")

# Check merged data
print("📌 Sample of merged data:")
print(df_merged.head())

# Show unmatched rows after merging
print("📌 Rows with unmatched `Neighborhood` (NaN `Location`):")
print(df_merged[df_merged["Location"].isnull()])

# Save cleaned data to CSV
df_merged.to_csv("cleaned_london_data.csv", index=False)
print("✅ Data cleaning complete. File saved as 'cleaned_london_data.csv'")

# Display dataset info
print("📌 Info summary of merged dataset:")
print(df_merged.info())

# Show descriptive statistics for numeric columns
print("\n📌 Descriptive statistics of key numerical columns:")
print(df_merged.describe())

# Final check for any remaining missing values
print("\n📌 Remaining missing values (if any):")
print(df_merged.isnull().sum())



