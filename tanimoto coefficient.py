
import pandas as pd
from rdkit import Chem
from rdkit.Chem import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
import warnings
from rdkit import RDLogger
import os

# Suppress RDKit warnings
RDLogger.DisableLog('rdApp.*')

input_directory = r"C:\Users\cmain\PycharmProjects\pythonProject"  # Ensure this is correct and points to your folder
output_directory = r"C:\Output"

# Function to calculate the Tanimoto coefficient between two SMILES strings
def calculate_tanimoto(smiles1, smiles2):
    try:
        mol1 = Chem.MolFromSmiles(smiles1)
        mol2 = Chem.MolFromSmiles(smiles2)
        if mol1 and mol2:  # Ensure both molecules are valid
            fp1 = FingerprintMols.FingerprintMol(mol1)
            fp2 = FingerprintMols.FingerprintMol(mol2)
            return DataStructs.FingerprintSimilarity(fp1, fp2)  # Tanimoto coefficient
        else:
            return None
    except Exception as e:
        print(f"Error calculating Tanimoto coefficient: {e}")
        return None


# Load the CSV files with dtype specification
try:
    csv1 = pd.read_csv(os.path.join(input_directory, 'traditionalmed.csv'), dtype={'chemicals': str, 'smiles': str})
    csv2 = pd.read_csv(os.path.join(input_directory, 'cleaned_drugdata.csv'), dtype={'cIds': str, 'smiles': str})

except FileNotFoundError as e:
    print(f"Error reading CSV file: {e}")
    exit()
except pd.errors.EmptyDataError as e:
    print(f"Error: Empty CSV file: {e}")
    exit()

# Prepare to resume if results already exist
results_file = 'tanimoto_similarity_scores.csv'
if os.path.exists(results_file):
    similarity_df = pd.read_csv(results_file)
    processed_drugs = set(similarity_df['Drug Name'])
else:
    similarity_df = pd.DataFrame()
    processed_drugs = set()

# Prepare a list for new results
all_rows = []

# Set the number of decimal places
decimal_places = 4

# Compare each SMILES in the first CSV with all SMILES in the second CSV

for index1, row1 in csv1.iterrows():
    drug_name = row1['drug_name']
    smiles1 = row1['smiles']

    # Skip already processed drugs
    if drug_name in processed_drugs:
        print(f"Skipping already processed drug: {drug_name}")
        continue

    # Create a row for the current 'Drug Name'
    similarity_row = {'Drug Name': drug_name}

    for index2, row2 in csv2.iterrows():
        chemical = row2['cIds']
        smiles2 = row2['smiles']

        # Calculate Tanimoto coefficient
        tanimoto_score = calculate_tanimoto(smiles1, smiles2)

        # Round the Tanimoto score before adding to the similarity_row
        similarity_row[chemical] = round(tanimoto_score, decimal_places) if tanimoto_score is not None else None

        # Print processing details
        print(f"Comparing '{drug_name}' with '{chemical}': Tanimoto Score = {similarity_row[chemical]}")

    # Collect each row in a list
    all_rows.append(similarity_row)

    # Convert the list of rows to a DataFrame and save periodically
    similarity_df = pd.DataFrame(all_rows)
    similarity_df.to_csv(results_file, index=False)

    # Print progress
    print(f"Processed drug {index1 + 1}/{len(csv1)}")

# Save the final result to a CSV file
try:
    similarity_df.to_csv(results_file, index=False)
    print(f"Tanimoto similarity scores have been calculated and saved to '{results_file}'.")
except Exception as e:
    print(f"Error saving CSV file: {e}")
