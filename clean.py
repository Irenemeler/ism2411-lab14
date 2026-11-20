
import pandas as pd

# SELF-ASSESSMENT
#
# 1. Which cleaning decisions were ambiguous?
# Filling missing quantities with the mean was an estimate,
# not necessarily the actual quantity sold. I would want
# original order records to confirm the missing values.
# I also kept missing region and customer_id values because
# they were not required to identify the orders.
#
# 2. Are the comments clear about why decisions were made?
# Yes. I explained why rows missing essential order information
# were removed, why missing quantities were filled with the mean,
# and why negative revenue was preserved.
#
# 3. What was the most unexpected finding?
# I was surprised by the maximum revenue of $59,994 and the
# negative revenue of -$3,268. These values show that some
# orders were unusually large or may have involved returns.

# EXERCISE 1: INSPECT THE DATA

df = pd.read_csv("data/messy_sales.csv")

print("ORIGINAL DATA INFORMATION")
df.info()

print("\nMISSING VALUES")
print(df.isnull().sum())


# EXERCISE 2: STANDARDIZE COLUMN NAMES

df.columns = df.columns.str.lower().str.replace(" ", "_")

print("\nUPDATED COLUMN NAMES")
print(df.columns.tolist())

# EXERCISE 3: HANDLE MISSING VALUES

print("\nSHAPE BEFORE CLEANING")
print(df.shape)

# Drop rows missing essential order information.
df = df.dropna(subset=["order_id", "order_date"])

# Fill missing quantities with the average quantity.
df["quantity_sold"] = df["quantity_sold"].fillna(
    df["quantity_sold"].mean()
)

print("\nSHAPE AFTER CLEANING")
print(df.shape)

print("\nMISSING VALUES AFTER CLEANING")
print(df.isnull().sum())

# EXERCISE 4: CONVERT DATA TYPES

# Convert order_date into datetime format.
df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce", format="mixed"
)

print("\nINVALID DATES")
print(df["order_date"].isna().sum())

# Remove dollar signs and commas, then convert prices to floats.
df["unit_price"] = (
    df["unit_price"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Convert quantity_sold to integers.
df["quantity_sold"] = df["quantity_sold"].astype(int)

# Calculate revenue and round to two decimal places.
df["revenue"] = (
    df["unit_price"] * df["quantity_sold"]
).round(2)

print("\nUPDATED DATA TYPES")
print(df.dtypes)

 # EXERCISE 5: REMOVE DUPLICATES

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

# Remove duplicate rows.
df = df.drop_duplicates()

print("\nSHAPE AFTER REMOVING DUPLICATES")
print(df.shape)

# EXERCISE 6: ANALYZE THE DATA

print("\nSUMMARY STATISTICS")
print(df.describe())

# Quantity sold has a suspicious maximum of 9999.
# This may be a placeholder or data-entry error rather than a real sale.
# Negative revenue is preserved because it may represent a customer return.

# Remove rows with the erroneous quantity placeholder.
df = df[df["quantity_sold"] != 9999]

print("\nSHAPE AFTER REMOVING ERRONEOUS QUANTITIES")
print(df.shape)

# EXERCISE 7: SAVE AND VERIFY CLEANED DATA

# Save the cleaned dataset without an extra index column.
df.to_csv("data/clean_sales.csv", index=False)

# Reload the cleaned CSV.
cleaned_df = pd.read_csv("data/clean_sales.csv")

print("\nRELOADED CLEANED DATA")
cleaned_df.info()

# Reload again while converting order_date to datetime.
cleaned_df_dates = pd.read_csv(
    "data/clean_sales.csv",
    parse_dates=["order_date"]
)

print("\nVERIFY ORDER DATE TYPE")
print(cleaned_df_dates["order_date"].dtype)