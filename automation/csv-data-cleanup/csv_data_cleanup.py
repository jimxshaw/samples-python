import pandas as pd

df = pd.read_csv('supplier_vulnerability_findings.csv')

# Display basic information about the DataFrame.
print("DF Info:")
print(df.info())
print()

# Display the first few rows of the DataFrame and check for missing values.
print("DF first few rows:")
print(df.head())
print()

# Check for missing values in each column.
print("Missing values in each Column:")
print(df.isnull().sum())
print()

# Check for unique values in the 'severity' column.
print(df["severity"].unique())
print()

# # Check for duplicate rows in the DataFrame.
# print(df.duplicated().sum())
# print()

# # Check for duplicate rows based on specific columns: 'finding_id', 'supplier_name', and 'severity'.
# print(df.duplicated(subset = ["finding_id", "supplier_name", "severity"]))
# print()

# # Check for duplicate rows based on specific columns: 'finding_id', 'supplier_name', and 'severity' and display them.
# print(df["supplier_name"].str.strip().str.lower())
# print()

df["supplier_name"] = df["supplier_name"].str.strip().str.lower()

print(df["supplier_name"].unique())
print()

df["severity"] = df["severity"].str.strip().str.lower()
print(df["severity"].unique())
print()

df["asset"] = df["asset"].fillna("unknown")
print(df["asset"].unique())
print()

df["severity"] = df["severity"].fillna("untriaged")
print(df["severity"].unique())
print()

print(df.duplicated(subset = ["supplier_name", "asset", "cve_id"]))
print()

print(df.duplicated(subset = ["supplier_name", "asset", "cve_id"]).sum())
print()

df_no_duplicates = df.drop_duplicates(subset = ["supplier_name", "asset", "cve_id"], keep = "first")
print(df_no_duplicates)
print()

severity_counts = df_no_duplicates["severity"].value_counts()
print("Severity Counts:")
print(severity_counts)
print()

df_no_duplicates.to_csv('supplier_vulnerability_findings_cleaned.csv', index = False)
