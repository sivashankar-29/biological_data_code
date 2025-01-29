import pandas as pd
import os

# Define the directory paths
input_directory = r"C:\Sys3"  # Ensure this is correct and points to your folder
output_directory = r"C:\Output"  # Ensure this is correct


# Load the CSV file
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"CSV file '{file_path}' loaded successfully.")

        # Clean up column names by stripping any leading/trailing spaces
        data.columns = data.columns.str.strip()

        # Print column names for debugging
        print(f"Columns in the CSV: {data.columns}")

        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None


# Remove rows with 0 or None values
def remove_zero_none_values(data):
    print("Removing rows with 0 or None values...")
    data_cleaned = data.dropna()  # Remove rows with NaN or None values
    data_cleaned = data_cleaned[(data_cleaned != 0).all(axis=1)]  # Remove rows with zero values
    print(f"Rows after removal: {len(data_cleaned)}")
    return data_cleaned


# Remove duplicate SMILES IDs
def remove_duplicate_smiles(data):
    # Ensure we are using the correct column for SMILES ('smiles' in your case)
    print("Removing duplicate SMILES IDs...")

    # If 'smiles' column exists, proceed
    if 'smiles' in data.columns:
        data_cleaned = data.drop_duplicates(subset='smiles', keep='first')  # Keep the first occurrence
        print(f"Number of duplicate SMILES removed: {len(data) - len(data_cleaned)}")
    else:
        print("Error: 'smiles' column not found.")
        exit()

    return data_cleaned


# Save the cleaned data to a new CSV file
def save_cleaned_csv(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Cleaned data saved to '{output_file}'.")
    except Exception as e:
        print(f"Error saving cleaned CSV: {e}")


# Main processing function
def process_data(input_file, output_file):
    # Load the data
    data = load_csv(input_file)
    if data is None:
        return

    # Clean the data
    data = remove_zero_none_values(data)
    data = remove_duplicate_smiles(data)

    # Save the cleaned data
    save_cleaned_csv(data, output_file)


# Define file paths
input_file = os.path.join(input_directory, "Drug_info.csv")  # Ensure the file exists at this location
output_file = os.path.join(output_directory, "cleaned_data.csv")  # Specify output file name

# Run the data processing function
process_data(input_file, output_file)
