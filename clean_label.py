import pandas as pd

# Load your data
input_path = "labeled_output.csv"  # replace with your actual file path
df = pd.read_csv(input_path)

# Remove rows with any empty (NaN) values
df_cleaned = df.dropna()

# Optionally, save the cleaned data to a new file
output_path = "cleaned_labeled_output.csv"  # replace with your desired output file path
df_cleaned.to_csv(output_path, index=False)

print(f"✅ Cleaned data saved to {output_path}")