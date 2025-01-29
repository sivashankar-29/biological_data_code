import csv
import os

def split_csv_file(input_file: str, output_folder: str, lines_per_file: int = 400):
    """
    Split a large CSV file into multiple smaller files, each with a specified number of lines,
    and save them in the specified output directory.

    :param input_file: Path to the input CSV file
    :param output_folder: Path to the output folder where files will be saved
    :param lines_per_file: Number of lines per split file
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    print(f"Files will be saved in: {output_folder}")

    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract the headers from the first row

        file_count = 0
        current_lines = []

        for i, row in enumerate(reader, start=1):
            current_lines.append(row)

            # Write to a new file when reaching the specified line count
            if i % lines_per_file == 0:
                output_file = os.path.join(output_folder, f"output_part_{file_count + 1}.csv")
                with open(output_file, mode='w', newline='', encoding='utf-8') as output:
                    writer = csv.writer(output)
                    writer.writerow(headers)  # Write the headers
                    writer.writerows(current_lines)

                file_count += 1
                current_lines = []

        # Write any remaining lines to a final file
        if current_lines:
            output_file = os.path.join(output_folder, f"output_part_{file_count + 1}.csv")
            with open(output_file, mode='w', newline='', encoding='utf-8') as output:
                writer = csv.writer(output)
                writer.writerow(headers)
                writer.writerows(current_lines)

    print(f"CSV file successfully split into {file_count + 1} parts.")

# Example usage
input_file_path = r"C:\Users\SIVASHANKAR S\OneDrive\Desktop\pythonproject\Drug_info.csv"
output_directory = r"C:\Users\SIVASHANKAR S\OneDrive\Desktop\output"
split_csv_file(input_file=input_file_path, output_folder=output_directory)
