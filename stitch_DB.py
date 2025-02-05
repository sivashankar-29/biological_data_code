import pandas as pd
import os

# Set the paths for the CSV file and the directory containing TSV files
csv_file = r'C:\Output\output_part_4.csv'  # Replace with your CSV file path
tsv_directory = r'C:\Users\cmain\PycharmProjects\pythonProject\New folder' # Directory containing TSV files
output_file = 'matched_data4.csv'

# Load the main CSV file
try:
    csv_data = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"CSV file '{csv_file}' not found.")
    exit()
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()

# Check for the presence of the necessary columns
if 'Drug Name' not in csv_data.columns:
    print("'Drug Name' column not found in CSV file. Exiting.")
    exit()

# Remove rows with NaN in 'Drug Name' column and reset index
csv_data = csv_data.dropna(subset=['Drug Name']).reset_index(drop=True)

# Track the matched names and initialize counters
matched_names = set()
total_matched_rows = 0  # Counter for total matched rows
match_count = 0  # Counter to keep track of matched names

# Check if output file already exists
if os.path.exists(output_file):
    os.remove(output_file)  # Remove the file if it exists to start fresh

# Prepare a list to hold the matched rows
matched_rows = []

# Iterate over all files in the TSV directory
for filename in os.listdir(tsv_directory):
    if filename.endswith('.tsv'):
        tsv_file = os.path.join(tsv_directory, filename)  # Get full path of the TSV file

        # Load the TSV file
        try:
            tsv_data = pd.read_csv(tsv_file, sep='\t')  # Specify tab as delimiter
        except Exception as e:
            print(f"Error loading TSV file '{tsv_file}': {e}")
            continue  # Skip to the next file if there's an error

        # Check for the presence of the 'name' column in TSV
        if 'name' not in tsv_data.columns:
            print(f"'name' column not found in TSV file '{filename}'. Skipping.")
            continue

        # Compare names in a case-insensitive manner
        for index, csv_row in csv_data.iterrows():
            drug_name = csv_row.get('Drug Name', None)

            # Normalize the drug name for case-insensitive comparison
            normalized_drug_name = str(drug_name).lower()  # Convert to string and lower case

            # Skip if this name is already matched
            if normalized_drug_name in matched_names:
                continue

            # Find matches in the TSV file
            matching_rows = tsv_data[tsv_data['name'].str.lower() == normalized_drug_name]

            if not matching_rows.empty:
                matched_names.add(normalized_drug_name)  # Add the matched name to the set
                match_count += 1  # Increment match counter

                # Append all matching rows to matched_rows
                for _, matched_row in matching_rows.iterrows():
                    matched_row_dict = {
                        'TMC_ID': csv_row.get('TMC_ID', None),  # Replace with your actual TMC_ID column name
                        'Drug Name': drug_name,
                        **matched_row.to_dict()  # Add entire matched row from TSV
                    }
                    matched_rows.append(matched_row_dict)
                    total_matched_rows += 1  # Increment total matched rows

                    # Print details of each matched entry
                    print("Matched Entry:")
                    print(matched_row_dict)
                    print()  # Print a newline for better readability

                # Check if all rows from CSV are matched
                if match_count == len(csv_data):
                    print("All rows in CSV file have been matched.")
                    break  # Exit the loop if all matches are found

        # Break the outer loop if all matches have been found
        if match_count == len(csv_data):
            break

# Create a DataFrame from matched rows
matched_df = pd.DataFrame(matched_rows)

# Save matched data to the output CSV file if there are matches
if not matched_df.empty:
    matched_df.to_csv(output_file, index=False)
    print(f"Matched data has been saved to '{output_file}'")
else:
    print("No matches found.")

# Print final counts
print(f"Processing complete. Total matched names count: {match_count}")
print(f"Total matched rows in output: {total_matched_rows}")
