import pandas as pd
import re
import sys
from pathlib import Path

def detect_11_digit_format(ndc):
    """
    Detect the format of an 11-digit NDC by finding where the zero was added
    """
    ndc_digits = re.sub(r'\D', '', str(ndc))

    if len(ndc_digits) != 11:
        return None, ndc_digits    # Check if first digit is 0 (likely 4-4-2 format)
    if ndc_digits[0] == '0' and ndc_digits[1] != '0':
        return '4-4-2', ndc_digits

    # Check if 6th digit is 0 (likely 5-3-2 format)
    if ndc_digits[5] == '0' and ndc_digits[6] != '0':
        return '5-3-2', ndc_digits

    # Check if 10th digit is 0 (likely 5-4-1 format)
    if ndc_digits[9] == '0' and ndc_digits[10] != '0':
        return '5-4-1', ndc_digits

    # If no clear pattern, return as unknown
    return 'unknown', ndc_digits

def detect_10_digit_format(ndc):
    """
    Detect the format of a 10-digit NDC (4-4-2, 5-3-2, or 5-4-1)
    """
    # Remove any non-digit characters
    ndc_digits = re.sub(r'\D', '', str(ndc))

    # Check if it's already 11 digits
    if len(ndc_digits) == 11:
        return None, ndc_digits

    # Check if it's not 10 digits
    if len(ndc_digits) != 10:
        return None, ndc

    # Try to detect format based on common patterns
    # This is a heuristic approach since we can't definitively know the format
    # without additional information

    # Check for 4-4-2 format (manufacturer code is 4 digits)
    # These typically start with lower numbers
    if ndc_digits[0] in ['0', '1', '2', '3']:
        return '4-4-2', ndc_digits

    # Check for 5-4-1 format (package code is 1 digit)
    # If the last segment would be 1 digit, it's likely 5-4-1
    if ndc_digits[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        # Additional check: if the 6th-9th digits form a reasonable product code
        product_code = ndc_digits[5:9]
        if int(product_code) < 9999:
            return '5-4-1', ndc_digits

    # Default to 5-3-2 format (most common)
    return '5-3-2', ndc_digits

def convert_10_to_11(ndc):
    """
    Convert a 10-digit NDC to 11-digit format
    """
    format_type, ndc_digits = detect_10_digit_format(ndc)

    if format_type is None:
        return ndc  # Return as-is if already 11 digits or invalid

    if format_type == '4-4-2':
        # Add 0 at the beginning
        return '0' + ndc_digits
    elif format_type == '5-3-2':
        # Add 0 at position 6 (index 5)
        return ndc_digits[:5] + '0' + ndc_digits[5:]
    elif format_type == '5-4-1':
        # Add 0 at position 10 (index 9)
        return ndc_digits[:9] + '0' + ndc_digits[9:]

    return ndc_digits

def convert_11_to_10(ndc):
    """
    Convert an 11-digit NDC to 10-digit format by removing the added zero
    """
    format_type, ndc_digits = detect_11_digit_format(ndc)

    if format_type is None:
        return ndc  # Return as-is if not 11 digits

    if format_type == '4-4-2':
        # Remove the first digit (0)
        return ndc_digits[1:]
    elif format_type == '5-3-2':
        # Remove the 6th digit (0)
        return ndc_digits[:5] + ndc_digits[6:]
    elif format_type == '5-4-1':
        # Remove the 10th digit (0)
        return ndc_digits[:9] + ndc_digits[10:]
    elif format_type == 'unknown':
        # Can't determine format, return with warning
        print(f"Warning: Could not determine format for NDC {ndc_digits}")
        return ndc_digits

    return ndc_digits

def process_file(input_file, ndc_column, conversion_type, output_file=None):
    """
    Process a CSV/Excel file and convert NDCs in the specified column
    """
    # Determine file type and read accordingly
    file_ext = Path(input_file).suffix.lower()

    try:
        if file_ext == '.csv':
            df = pd.read_csv(input_file)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(input_file)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Check if column exists
    if ndc_column not in df.columns:
        print(f"Error: Column '{ndc_column}' not found in the file.")
        print(f"Available columns: {', '.join(df.columns)}")
        return

    # Create a new column for converted NDCs
    if conversion_type == '10to11':
        converted_column = f"{ndc_column}_11digit"
        df[converted_column] = df[ndc_column].apply(convert_10_to_11)
    else:  # 11to10
        converted_column = f"{ndc_column}_10digit"
        df[converted_column] = df[ndc_column].apply(convert_11_to_10)

    # Create output filename if not specified
    if output_file is None:
        output_file = Path(input_file).stem + "_converted" + Path(input_file).suffix

    # Save the result
    try:
        if file_ext == '.csv':
            df.to_csv(output_file, index=False)
        else:
            df.to_excel(output_file, index=False)
        print(f"Successfully converted NDCs and saved to: {output_file}")

        # Show summary
        print(f"\nConversion Summary:")
        print(f"Total rows processed: {len(df)}")
        print(f"Conversion type: {conversion_type}")
        print(f"Original NDC column: {ndc_column}")
        print(f"Converted NDC column: {converted_column}")

        # Show sample conversions
        print(f"\nSample conversions (first 5):")
        sample_df = df[[ndc_column, converted_column]].head()
        for idx, row in sample_df.iterrows():
            print(f"  {row[ndc_column]} → {row[converted_column]}")

    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    """
    Main function to handle user input and process the file
    """
    print("NDC Format Converter (10↔11 digits)")
    print("=" * 40)

    # Get conversion type
    print("\nSelect conversion type:")
    print("1. Convert 10-digit to 11-digit")
    print("2. Convert 11-digit to 10-digit")

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == '1':
            conversion_type = '10to11'
            break
        elif choice == '2':
            conversion_type = '11to10'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Get input file
    input_file = input("\nEnter the path to your input file (CSV or Excel): ").strip()

    if not Path(input_file).exists():
        print(f"Error: File '{input_file}' not found.")
        return

    # Show available columns
    file_ext = Path(input_file).suffix.lower()
    try:
        if file_ext == '.csv':
            df = pd.read_csv(input_file, nrows=5)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(input_file, nrows=5)
        else:
            print(f"Error: Unsupported file type '{file_ext}'. Please use CSV or Excel files.")
            return

        print(f"\nAvailable columns in the file:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")

    except Exception as e:
        print(f"Error reading file: {e}")
        return    # Get NDC column
    while True:
        choice = input("\nEnter the number of the column containing NDCs: ").strip()
        try:
            col_index = int(choice) - 1
            if 0 <= col_index < len(df.columns):
                ndc_column = df.columns[col_index]
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(df.columns)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get output file (optional)
    output_name = input("\nEnter output filename without extension (press Enter to use default): ").strip()
    if output_name:
        output_file = output_name + file_ext
    else:
        output_file = None

    # Process the file
    print("\nProcessing...")
    process_file(input_file, ndc_column, conversion_type, output_file)

if __name__ == "__main__":
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        if len(sys.argv) < 4:
            print("Usage: python ndc_converter.py <input_file> <ndc_column> <conversion_type> [output_file]")
            print("  conversion_type: '10to11' or '11to10'")
            print("\nExample:")
            print("  python ndc_converter.py medications.csv NDC_Code 10to11")
            print("  python ndc_converter.py medications.csv NDC_Code 11to10 output.csv")
            sys.exit(1)

        input_file = sys.argv[1]
        ndc_column = sys.argv[2]
        conversion_type = sys.argv[3]

        if conversion_type not in ['10to11', '11to10']:
            print("Error: conversion_type must be '10to11' or '11to10'")
            sys.exit(1)

        output_file = sys.argv[4] if len(sys.argv) > 4 else None

        process_file(input_file, ndc_column, conversion_type, output_file)
    else:
        # Interactive mode
        main()